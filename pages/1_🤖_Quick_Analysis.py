"""
Quick AI-Powered Analysis Page
One-click automated analysis with AI insights
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from components.participant_selector import participant_selector, show_participant_summary
from utils.data_loader import load_multiple_participants
from utils.ai_assistant import generate_ai_insights, suggest_visualizations, detect_anomalies, generate_comparison_insights
from utils.statistical_analysis import compare_participants
from utils.chart_factory import create_custom_chart
from utils.export_helpers import export_chart_as_png, export_chart_as_pdf, export_data_as_csv, create_filename
from config.settings import METRIC_LABELS

st.set_page_config(page_title="Quick AI Analysis", page_icon="🤖", layout="wide")

# ============ AUTHENTICATION ============
from utils.auth import check_authentication, show_user_info, logout_button

if not check_authentication():
    st.stop()

show_user_info()
logout_button()
# ========================================

st.title("🤖 Quick AI-Powered Analysis")
st.markdown("Let AI do the heavy lifting. Just select participants and click analyze!")

# Sidebar for participant selection
with st.sidebar:
    st.header("1️⃣ Select Participants")
    
    selected_participants = participant_selector(mode="mixed", key_prefix="quick")
    
    st.divider()
    
    if selected_participants:
        show_participant_summary(selected_participants)
        
        st.divider()
        
        # Date range selection
        st.subheader("2️⃣ Date Range (Optional)")
        use_custom_range = st.checkbox("Use custom date range", key="quick_custom_date")
        
        if use_custom_range:
            import datetime
            # Simplified layout for sidebar - no columns
            start_date = st.date_input(
                "Start Date",
                value=datetime.date(2023, 6, 1),
                key="quick_start_date"
            )
            end_date = st.date_input(
                "End Date",
                value=datetime.date(2023, 8, 31),
                key="quick_end_date"
            )
            date_range = (start_date, end_date)
        else:
            date_range = None

# Main content area
if not selected_participants:
    st.info("👈 Please select participants from the sidebar to begin")
    
    # Show example
    with st.expander("📖 Example: What will I see?"):
        st.markdown("""
        When you run Quick AI Analysis, you'll get:
        
        1. **AI-Generated Summary** - Natural language insights about patterns
        2. **Automatic Visualizations** - Charts suggested by AI based on your data
        3. **Statistical Analysis** - T-tests, effect sizes, significance tests
        4. **Anomaly Detection** - Automatic identification of unusual patterns
        5. **Recommendations** - Follow-up analyses suggested by AI
        
        All of this happens automatically with one click!
        """)
    
    st.stop()

# Run analysis button
if st.button("🚀 Run Smart Analysis", type="primary", use_container_width=True):
    
    with st.spinner("🤖 AI is analyzing your data... This takes ~10 seconds"):
        
        # Load data
        data = load_multiple_participants(
            selected_participants,
            date_range=date_range if use_custom_range else None
        )
        
        if data.empty:
            st.error("No data found for selected participants")
            st.stop()
        
        # Store in session state
        st.session_state.quick_analysis_data = data
        st.session_state.quick_analysis_participants = selected_participants
        
        # Detect if we have OCD vs Control comparison
        has_ocd = any(data['participant_type'] == 'OCD')
        has_control = any(data['participant_type'] == 'Control')
        is_comparison = has_ocd and has_control
        
        st.success("✅ Analysis Complete!")
        
        # Tab layout for results
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 AI Insights",
            "📊 Visualizations",
            "📈 Statistical Tests",
            "⚠️ Anomalies"
        ])
        
        with tab1:
            st.subheader("AI-Generated Insights")
            
            if is_comparison:
                # Comparison mode
                ocd_data = data[data['participant_type'] == 'OCD']
                control_data = data[data['participant_type'] == 'Control']
                
                # Run statistical comparison
                stats_results = compare_participants(
                    ocd_data,
                    control_data,
                    ['minutesAsleep', 'efficiency', 'steps', 'heart_rate']
                )
                
                # Generate AI insights for comparison
                insights = generate_comparison_insights(ocd_data, control_data, stats_results)
                st.markdown(insights)
                
            else:
                # Single participant or group of same type
                for pid in selected_participants:
                    participant_data = data[data['participantId'] == pid]
                    insights = generate_ai_insights(participant_data)
                    
                    with st.expander(f"📄 Insights for {pid}", expanded=True):
                        st.markdown(insights)
        
        with tab2:
            st.subheader("AI-Suggested Visualizations")
            
            # Get AI suggestions for charts
            metrics_to_analyze = ['minutesAsleep', 'efficiency', 'steps', 'heart_rate']
            suggestions = suggest_visualizations(
                selected_participants,
                metrics_to_analyze,
                data
            )
            
            st.info(f"💡 AI generated {len(suggestions)} visualization suggestions based on your data")
            
            for i, suggestion in enumerate(suggestions):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"### {i+1}. {suggestion['title']}")
                        st.caption(f"**Why suggested:** {suggestion['reason']}")
                    
                    with col2:
                        priority_emoji = "🔴" if suggestion['priority'] == 'high' else "🟡" if suggestion['priority'] == 'medium' else "🟢"
                        st.caption(f"{priority_emoji} Priority: {suggestion['priority'].upper()}")
                    
                    # Create the chart
                    chart_config = {
                        'type': suggestion['type'],
                        'data': data,
                        'x': suggestion.get('x', 'date'),
                        'y': suggestion.get('y', metrics_to_analyze[0]),
                        'color_by': suggestion.get('color_by'),
                        'title': suggestion['title']
                    }
                    
                    fig = create_custom_chart(chart_config)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export buttons
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
                    
                    with col1:
                        # Export PNG
                        try:
                            img_bytes, filename = export_chart_as_png(
                                fig, 
                                create_filename(suggestion['title'], 'png', selected_participants)
                            )
                            st.download_button(
                                label="💾 PNG",
                                data=img_bytes,
                                file_name=filename,
                                mime="image/png",
                                key=f"export_png_{i}",
                                use_container_width=True
                            )
                        except Exception as e:
                            if st.button("💾 PNG", key=f"export_png_{i}", use_container_width=True):
                                st.error(f"PNG export requires 'kaleido' package. Install with: pip install kaleido")
                    
                    with col2:
                        # Export PDF
                        try:
                            pdf_bytes, filename = export_chart_as_pdf(
                                fig,
                                create_filename(suggestion['title'], 'pdf', selected_participants)
                            )
                            st.download_button(
                                label="📄 PDF",
                                data=pdf_bytes,
                                file_name=filename,
                                mime="application/pdf",
                                key=f"export_pdf_{i}",
                                use_container_width=True
                            )
                        except Exception as e:
                            if st.button("📄 PDF", key=f"export_pdf_{i}", use_container_width=True):
                                st.error(f"PDF export requires 'kaleido' package. Install with: pip install kaleido")
                    
                    with col3:
                        # Export Data as CSV
                        csv_data, filename = export_data_as_csv(
                            data,
                            create_filename(suggestion['title'], 'csv', selected_participants)
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
        
        with tab3:
            st.subheader("Statistical Analysis")
            
            if is_comparison:
                # Show statistical comparison
                ocd_data = data[data['participant_type'] == 'OCD']
                control_data = data[data['participant_type'] == 'Control']
                
                stats_results = compare_participants(
                    ocd_data,
                    control_data,
                    ['minutesAsleep', 'minutesAwake', 'efficiency', 'timeInBed', 'steps', 'heart_rate']
                )
                
                # Summary
                st.markdown("### 📊 Comparison Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Metrics Compared",
                        stats_results['summary']['total_metrics']
                    )
                
                with col2:
                    st.metric(
                        "Significant Findings",
                        stats_results['summary']['significant_findings'],
                        delta=f"{stats_results['summary']['percentage_significant']}%"
                    )
                
                with col3:
                    significance_level = "High" if stats_results['summary']['percentage_significant'] > 50 else "Medium" if stats_results['summary']['percentage_significant'] > 25 else "Low"
                    st.metric(
                        "Significance Level",
                        significance_level
                    )
                
                st.divider()
                
                # Detailed results table
                st.markdown("### 📋 Detailed Results")
                
                for result in stats_results['metrics']:
                    metric_name = METRIC_LABELS.get(result['metric'], result['metric'])
                    
                    with st.expander(f"{'✅' if result['significant'] else '➖'} {metric_name}", expanded=result['significant']):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**🔴 OCD Group**")
                            st.metric("Mean", f"{result['ocd_mean']:.2f}")
                            st.caption(f"SD: {result['ocd_std']:.2f} | n={result['ocd_n']}")
                        
                        with col2:
                            st.markdown("**🟢 Control Group**")
                            st.metric("Mean", f"{result['control_mean']:.2f}")
                            st.caption(f"SD: {result['control_std']:.2f} | n={result['control_n']}")
                        
                        with col3:
                            st.markdown("**📊 Statistics**")
                            st.metric(
                                "Difference",
                                f"{result['difference']:.2f}",
                                delta=f"{result['percent_difference']:.1f}%"
                            )
                            st.caption(f"p-value: {result['p_value']:.4f}")
                            st.caption(f"Effect size (d): {result['cohens_d']:.3f} ({result['effect_size_interpretation']})")
                        
                        if result['significant']:
                            st.success(f"✅ Statistically significant difference (p < 0.05)")
                        else:
                            st.info("No significant difference detected")
            
            else:
                st.info("Statistical comparison requires both OCD and Control participants")
        
        with tab4:
            st.subheader("Anomaly Detection")
            
            anomalies_found = False
            
            for pid in selected_participants:
                participant_data = data[data['participantId'] == pid]
                anomalies = detect_anomalies(participant_data)
                
                if anomalies:
                    anomalies_found = True
                    st.markdown(f"### ⚠️ Anomalies for {pid}")
                    
                    for anomaly in anomalies:
                        severity_color = "🔴" if anomaly['severity'] == 'high' else "🟡"
                        
                        with st.expander(f"{severity_color} {anomaly['metric']} - {anomaly['type'].title()}", expanded=anomaly['severity'] == 'high'):
                            st.warning(anomaly['description'])
                            
                            if 'dates' in anomaly:
                                st.caption(f"**Affected dates:** {', '.join(anomaly['dates'])}")
                            
                            if 'recommendation' in anomaly:
                                st.info(f"**💡 Recommendation:** {anomaly['recommendation']}")
                    
                    st.divider()
            
            if not anomalies_found:
                st.success("✅ No significant anomalies detected in the selected data!")

else:
    # Show info about what will happen
    st.markdown("""
    ### Ready to analyze!
    
    Click the **"Run Smart Analysis"** button above to:
    
    - 🤖 Generate AI insights about patterns and trends
    - 📊 Create recommended visualizations automatically
    - 📈 Run statistical tests (if comparing OCD vs Control)
    - ⚠️ Detect anomalies and unusual patterns
    - 💡 Get follow-up recommendations
    
    **Selected:** {count} participant(s)
    """.format(count=len(selected_participants)))
    
    st.info("💡 Tip: For best results, select at least one OCD and one Control participant")

