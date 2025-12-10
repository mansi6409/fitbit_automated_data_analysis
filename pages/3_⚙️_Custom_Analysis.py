"""
Custom Analysis Page
Full manual control over all visualization parameters
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_multiple_participants, get_available_participants
from utils.chart_factory import create_custom_chart, apply_custom_styling
from utils.statistical_analysis import calculate_summary_statistics, calculate_correlation
from utils.export_helpers import export_chart_as_png, export_chart_as_pdf, export_data_as_csv, create_filename
from config.settings import AVAILABLE_METRICS, METRIC_LABELS, CHART_TYPES, COLOR_PALETTES

st.set_page_config(page_title="Custom Analysis", page_icon="⚙️", layout="wide")

# ============ AUTHENTICATION ============
from utils.auth import check_authentication, show_user_info, logout_button

if not check_authentication():
    st.stop()

show_user_info()
logout_button()
# ========================================

st.title("⚙️ Custom Visualization Builder")
st.markdown("Full control - build your charts exactly how you want them")

# Two column layout
sidebar_col, main_col = st.columns([1, 3])

with sidebar_col:
    st.markdown("### 📋 Configuration Panel")
    
    # Section 1: Data Selection
    with st.expander("1️⃣ Data Selection", expanded=True):
        all_participants = get_available_participants()
        
        st.markdown("**Participants**")
        selected_participants = st.multiselect(
            "Select participants",
            options=[p['id'] for p in all_participants],
            default=[all_participants[0]['id'], all_participants[1]['id']] if len(all_participants) >= 2 else [],
            format_func=lambda x: f"{x} ({'OCD' if any(p['id'] == x and p['type'] == 'OCD' for p in all_participants) else 'Control'})",
            label_visibility="collapsed"
        )
        
        st.markdown("**Date Range**")
        use_custom_date = st.checkbox("Custom date range", value=False, key="custom_date_range")
        
        if use_custom_date:
            import datetime
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start", datetime.date(2023, 6, 1), key="custom_start")
            with col2:
                end_date = st.date_input("End", datetime.date(2023, 8, 31), key="custom_end")
            date_range = (start_date, end_date)
        else:
            date_range = None
    
    # Section 2: Chart Configuration
    with st.expander("2️⃣ Chart Type", expanded=True):
        chart_type = st.selectbox(
            "Select chart type",
            options=CHART_TYPES,
            key="chart_type_select",
            label_visibility="collapsed"
        )
        
        chart_type_mapping = {
            "Line Chart": "line_chart",
            "Bar Chart": "bar_chart",
            "Scatter Plot": "scatter_plot",
            "Box Plot": "box_plot",
            "Violin Plot": "violin_plot",
            "Area Chart": "area_chart",
            "Histogram": "histogram",
            "Heatmap": "heatmap"
        }
        
        chart_type_key = chart_type_mapping.get(chart_type, "line_chart")
    
    # Section 3: Metrics
    with st.expander("3️⃣ Metrics", expanded=True):
        # For histograms, X-axis should be a numeric metric, not date
        if chart_type == "Histogram":
            x_axis = st.selectbox(
                "Metric (for distribution)",
                options=AVAILABLE_METRICS,
                format_func=lambda x: METRIC_LABELS.get(x, x),
                key="x_axis_select",
                help="Select the metric to analyze its distribution"
            )
            y_axis = None  # Histograms don't use Y-axis
        else:
            x_axis = st.selectbox(
                "X-Axis",
                options=['date'] + AVAILABLE_METRICS,
                format_func=lambda x: "Date" if x == 'date' else METRIC_LABELS.get(x, x),
                key="x_axis_select"
            )
            
            y_axis_options = AVAILABLE_METRICS
            y_axis = st.selectbox(
                "Y-Axis",
                options=y_axis_options,
                format_func=lambda x: METRIC_LABELS.get(x, x),
                key="y_axis_select"
            )
    
    # Section 4: Styling
    with st.expander("4️⃣ Styling Options"):
        chart_title = st.text_input(
            "Chart Title",
            value=f"{chart_type}: {METRIC_LABELS.get(y_axis if chart_type != 'Histogram' else x_axis, y_axis if chart_type != 'Histogram' else x_axis)}",
            key="chart_title"
        )
        
        color_scheme = st.selectbox(
            "Color Palette",
            options=list(COLOR_PALETTES.keys()),
            key="color_palette"
        )
        
        show_legend = st.checkbox("Show Legend", value=True, key="show_legend")
        show_grid = st.checkbox("Show Grid Lines", value=True, key="show_grid")
    
    # Section 5: Advanced Options
    with st.expander("5️⃣ Advanced Options"):
        # Color by option
        color_by = st.selectbox(
            "Color by",
            options=[None, 'participant_type', 'participantId'],
            format_func=lambda x: "None" if x is None else "Participant Type" if x == 'participant_type' else "Participant ID",
            key="color_by"
        )
        
        # Statistical overlays
        if chart_type in ["Line Chart", "Scatter Plot"]:
            show_trendline = st.checkbox("Show Trend Line", value=False, key="show_trend")
        else:
            show_trendline = False

with main_col:
    if not selected_participants:
        st.info("👈 Select participants from the configuration panel to start building your chart")
        
        # Show tips
        st.markdown("""
        ### 💡 Tips for Custom Analysis
        
        - **Start with data selection**: Choose participants and metrics
        - **Pick the right chart type**: Different types reveal different patterns
        - **Use color coding**: Color by participant type for easy comparison
        - **Try multiple views**: Create several charts to explore your data fully
        
        ### 📊 Available Chart Types
        
        - **Line Chart**: Best for time series and trends
        - **Bar Chart**: Compare values across categories
        - **Scatter Plot**: Reveal correlations between metrics
        - **Box Plot**: Show distribution and outliers
        - **Violin Plot**: Detailed distribution visualization
        - **Histogram**: Data distribution analysis
        """)
    
    else:
        # Load data
        with st.spinner("Loading data..."):
            data = load_multiple_participants(selected_participants, date_range)
        
        if data.empty:
            st.error("No data available for selected participants and date range")
            st.stop()
        
        # Show data summary
        with st.expander("📊 Data Summary"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", len(data))
            
            with col2:
                st.metric("Date Range", f"{data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
            
            with col3:
                st.metric("Participants", data['participantId'].nunique())
        
        st.divider()
        
        # Create chart
        st.markdown("### 📈 Live Preview")
        
        try:
            chart_config = {
                'type': chart_type_key,
                'data': data,
                'x': x_axis,
                'y': y_axis if chart_type != "Histogram" else None,
                'color_by': color_by,
                'title': chart_title,
                'show_trendline': show_trendline
            }
            
            fig = create_custom_chart(chart_config)
            
            # Apply custom styling
            styling_config = {
                'colors': COLOR_PALETTES.get(color_scheme),
                'show_grid': show_grid,
            }
            
            fig = apply_custom_styling(fig, styling_config)
            
            if not show_legend:
                fig.update_layout(showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
            st.exception(e)
        
        st.divider()
        
        # Action buttons
        st.markdown("### 🎬 Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Configuration", use_container_width=True):
                st.success("Configuration saved! (Feature coming soon)")
        
        with col2:
            # Export PNG
            try:
                img_bytes, filename = export_chart_as_png(
                    fig,
                    create_filename(chart_config.get('title', 'chart'), 'png', selected_participants)
                )
                st.download_button(
                    label="📥 PNG",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png",
                    key="export_png_custom",
                    use_container_width=True
                )
            except Exception as e:
                if st.button("📥 PNG", key="export_png_btn", use_container_width=True):
                    st.error("PNG export requires 'kaleido' package. Install with: pip install kaleido")
        
        with col3:
            # Export PDF
            try:
                pdf_bytes, filename = export_chart_as_pdf(
                    fig,
                    create_filename(chart_config.get('title', 'chart'), 'pdf', selected_participants)
                )
                st.download_button(
                    label="📄 PDF",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    key="export_pdf_custom",
                    use_container_width=True
                )
            except Exception as e:
                if st.button("📄 PDF", key="export_pdf_btn", use_container_width=True):
                    st.error("PDF export requires 'kaleido' package. Install with: pip install kaleido")
        
        with col4:
            # Export CSV
            csv_data, filename = export_data_as_csv(
                data,
                create_filename(chart_config.get('title', 'chart'), 'csv', selected_participants)
            )
            st.download_button(
                label="📊 CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                key="export_csv_custom",
                use_container_width=True
            )
        
        # Additional analysis section
        st.divider()
        st.markdown("### 🔍 Additional Analysis")
        
        tab1, tab2 = st.tabs(["Summary Statistics", "Correlation Analysis"])
        
        with tab1:
            st.markdown("#### Summary Statistics")
            
            for metric in [y_axis] if chart_type != "Histogram" else [x_axis]:
                if metric in data.columns:
                    stats = calculate_summary_statistics(data, metric)
                    
                    if stats:
                        st.markdown(f"**{METRIC_LABELS.get(metric, metric)}**")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Mean", f"{stats['mean']:.2f}")
                            st.caption(f"Median: {stats['median']:.2f}")
                        
                        with col2:
                            st.metric("Std Dev", f"{stats['std']:.2f}")
                            st.caption(f"Count: {stats['count']}")
                        
                        with col3:
                            st.metric("Min", f"{stats['min']:.2f}")
                            st.caption(f"Q25: {stats['q25']:.2f}")
                        
                        with col4:
                            st.metric("Max", f"{stats['max']:.2f}")
                            st.caption(f"Q75: {stats['q75']:.2f}")
                        
                        st.divider()
        
        with tab2:
            st.markdown("#### Correlation Analysis")
            
            if len(AVAILABLE_METRICS) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    metric1 = st.selectbox(
                        "Metric 1",
                        options=AVAILABLE_METRICS,
                        format_func=lambda x: METRIC_LABELS.get(x, x),
                        key="corr_metric1"
                    )
                
                with col2:
                    metric2 = st.selectbox(
                        "Metric 2",
                        options=[m for m in AVAILABLE_METRICS if m != metric1],
                        format_func=lambda x: METRIC_LABELS.get(x, x),
                        key="corr_metric2"
                    )
                
                if st.button("Calculate Correlation"):
                    corr_result = calculate_correlation(data, metric1, metric2)
                    
                    if corr_result:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Correlation (r)", f"{corr_result['correlation']:.3f}")
                        
                        with col2:
                            st.metric("P-value", f"{corr_result['p_value']:.4f}")
                        
                        with col3:
                            st.metric("Strength", corr_result['interpretation'])
                        
                        if corr_result['significant']:
                            st.success("✅ Statistically significant correlation (p < 0.05)")
                        else:
                            st.info("No significant correlation detected")

