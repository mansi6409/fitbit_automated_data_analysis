"""
Guided Analysis Page
AI-assisted manual analysis with recommendations
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components.participant_selector import participant_selector, show_participant_summary
from utils.data_loader import load_multiple_participants
from utils.ai_assistant import suggest_visualizations, generate_ai_insights
from utils.chart_factory import create_custom_chart
from utils.export_helpers import export_chart_as_png, export_chart_as_pdf, export_data_as_csv, create_filename
from config.settings import AVAILABLE_METRICS, METRIC_LABELS, CHART_TYPES

st.set_page_config(page_title="Guided Analysis", page_icon="🎯", layout="wide")

# ============ AUTHENTICATION ============
from utils.auth import check_authentication, show_user_info, logout_button

if not check_authentication():
    st.stop()

show_user_info()
logout_button()
# ========================================

st.title("🎯 Guided Analysis Mode")
st.markdown("AI suggests the path, you make the decisions")

# Initialize session state
if 'guided_step' not in st.session_state:
    st.session_state.guided_step = 1
if 'guided_participants' not in st.session_state:
    st.session_state.guided_participants = []
if 'guided_metrics' not in st.session_state:
    st.session_state.guided_metrics = []

# Progress indicator
progress = st.session_state.guided_step / 4
st.progress(progress, text=f"Step {st.session_state.guided_step} of 4")

st.divider()

# Step 1: Select Participants
if st.session_state.guided_step >= 1:
    st.subheader("Step 1: Select Participants")
    
    selected_participants = participant_selector(mode="mixed", key_prefix="guided")
    
    if selected_participants:
        show_participant_summary(selected_participants)
        st.session_state.guided_participants = selected_participants
        
        if st.button("✅ Continue to Step 2", type="primary"):
            st.session_state.guided_step = 2
            st.rerun()
    else:
        st.info("Select at least one participant to continue")

# Step 2: Select Metrics
if st.session_state.guided_step >= 2:
    st.divider()
    st.subheader("Step 2: Select Metrics to Analyze")
    
    # AI suggestion based on participant selection
    has_ocd = len([p for p in st.session_state.guided_participants if 'BK' in p or 'BW' in p or 'BX' in p]) > 0
    has_control = len(st.session_state.guided_participants) > len([p for p in st.session_state.guided_participants if 'BK' in p or 'BW' in p or 'BX' in p])
    
    if has_ocd and has_control:
        st.info("💡 **AI Suggestion:** You've selected both OCD and Control participants. We recommend analyzing sleep-related metrics as they often show significant differences.")
        suggested_metrics = ['minutesAsleep', 'efficiency', 'steps', 'heart_rate']
    else:
        st.info("💡 **AI Suggestion:** For time-series analysis, we recommend including sleep duration, efficiency, and activity metrics.")
        suggested_metrics = ['minutesAsleep', 'timeInBed', 'steps']
    
    selected_metrics = st.multiselect(
        "Select metrics to analyze",
        options=AVAILABLE_METRICS,
        default=suggested_metrics,
        format_func=lambda x: METRIC_LABELS.get(x, x),
        key="guided_metrics_select"
    )
    
    if selected_metrics:
        st.session_state.guided_metrics = selected_metrics
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Step 1"):
                st.session_state.guided_step = 1
                st.rerun()
        with col2:
            if st.button("✅ Continue to Step 3", type="primary"):
                st.session_state.guided_step = 3
                st.rerun()
    else:
        st.warning("Please select at least one metric")

# Step 3: Choose Visualizations
if st.session_state.guided_step >= 3:
    st.divider()
    st.subheader("Step 3: Select Visualizations")
    
    # Load data to get AI suggestions
    data = load_multiple_participants(st.session_state.guided_participants)
    
    # Get AI suggestions
    suggestions = suggest_visualizations(
        st.session_state.guided_participants,
        st.session_state.guided_metrics,
        data
    )
    
    st.markdown("### 💡 AI-Recommended Charts")
    st.caption("These charts are suggested based on your data. You can include/exclude any of them.")
    
    selected_charts = []
    
    for i, suggestion in enumerate(suggestions):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            include = st.checkbox(
                f"**{suggestion['title']}**",
                value=True,
                key=f"include_chart_{i}"
            )
            st.caption(f"📊 Type: {suggestion['type'].replace('_', ' ').title()} | Reason: {suggestion['reason']}")
        
        with col2:
            st.markdown(f"**Priority:** {suggestion['priority'].upper()}")
        
        if include:
            selected_charts.append(suggestion)
        
        st.divider()
    
    if selected_charts:
        st.session_state.guided_selected_charts = selected_charts
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Step 2", key="back_step2"):
                st.session_state.guided_step = 2
                st.rerun()
        with col2:
            if st.button("✅ Generate Analysis", type="primary"):
                st.session_state.guided_step = 4
                st.rerun()

# Step 4: View Results
if st.session_state.guided_step >= 4:
    st.divider()
    st.subheader("Step 4: Analysis Results")
    
    # Load data
    data = load_multiple_participants(st.session_state.guided_participants)
    
    # Generate visualizations
    st.markdown("### 📊 Your Visualizations")
    
    for i, chart_config in enumerate(st.session_state.guided_selected_charts):
        with st.container():
            st.markdown(f"#### {i+1}. {chart_config['title']}")
            
            # Build full config
            full_config = {
                'type': chart_config['type'],
                'data': data,
                'x': chart_config.get('x', 'date'),
                'y': chart_config.get('y', st.session_state.guided_metrics[0]),
                'color_by': chart_config.get('color_by'),
                'title': chart_config['title']
            }
            
            fig = create_custom_chart(full_config)
            st.plotly_chart(fig, use_container_width=True)
            
            # Action buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button("🤖 AI Insights", key=f"ai_insight_{i}", use_container_width=True):
                    with st.spinner("Generating insights..."):
                        insights = generate_ai_insights(data)
                        st.info(insights[:500] + "...")  # Show preview
            
            with col2:
                # Export PNG
                try:
                    img_bytes, filename = export_chart_as_png(
                        fig,
                        create_filename(chart_config['title'], 'png', st.session_state.guided_participants)
                    )
                    st.download_button(
                        label="💾 PNG",
                        data=img_bytes,
                        file_name=filename,
                        mime="image/png",
                        key=f"export_png_{i}",
                        use_container_width=True
                    )
                except:
                    if st.button("💾 PNG", key=f"export_png_{i}", use_container_width=True):
                        st.error("PNG export requires 'kaleido' package")
            
            with col3:
                # Export PDF
                try:
                    pdf_bytes, filename = export_chart_as_pdf(
                        fig,
                        create_filename(chart_config['title'], 'pdf', st.session_state.guided_participants)
                    )
                    st.download_button(
                        label="📄 PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"export_pdf_{i}",
                        use_container_width=True
                    )
                except:
                    if st.button("📄 PDF", key=f"export_pdf_{i}", use_container_width=True):
                        st.error("PDF export requires 'kaleido' package")
            
            with col4:
                # Export CSV
                csv_data, filename = export_data_as_csv(
                    data,
                    create_filename(chart_config['title'], 'csv', st.session_state.guided_participants)
                )
                st.download_button(
                    label="📊 CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    key=f"export_csv_{i}",
                    use_container_width=True
                )
            
            st.divider()
    
    # Option to start over
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Step 3"):
            st.session_state.guided_step = 3
            st.rerun()
    with col2:
        if st.button("🔄 Start New Analysis"):
            st.session_state.guided_step = 1
            st.session_state.guided_participants = []
            st.session_state.guided_metrics = []
            st.rerun()

