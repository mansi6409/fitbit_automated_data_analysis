"""
Chart creation using Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_line_chart(data, x, y, color_by=None, title="", **kwargs):
    """Create a line chart"""
    # Remove show_trendline if present (not applicable to line charts)
    kwargs = {k: v for k, v in kwargs.items() if k != 'show_trendline'}
    
    # Sort data by x-axis and color_by (if present) to ensure proper line connections
    sort_cols = [x, color_by] if color_by and color_by in data.columns else [x]
    data_sorted = data.sort_values(by=sort_cols).copy()
    
    # Auto-detect participant column if not specified
    if not color_by or color_by not in data_sorted.columns:
        if 'participant' in data_sorted.columns:
            color_by = 'participant'
        elif 'participantId' in data_sorted.columns:
            color_by = 'participantId'
        elif 'participant_type' in data_sorted.columns and data_sorted['participant_type'].nunique() > 1:
            color_by = 'participant_type'
        else:
            # Only one participant, no need for color grouping
            color_by = None
    
    fig = px.line(
        data_sorted,
        x=x,
        y=y,
        color=color_by,
        title=title,
        markers=True,
        **kwargs
    )
    
    fig.update_layout(
        hovermode='x unified',
        showlegend=True if color_by else False,
        height=500,
        xaxis=dict(
            rangeslider=dict(visible=False),
            type='date' if 'date' in str(x).lower() else 'linear'
        )
    )
    
    # Improve line appearance
    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=6)
    )
    
    return fig

def create_bar_chart(data, x, y, color_by=None, title="", **kwargs):
    """Create a bar chart"""
    # Remove show_trendline if present (not applicable to bar charts)
    kwargs = {k: v for k, v in kwargs.items() if k != 'show_trendline'}
    
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color_by,
        title=title,
        barmode='group',
        **kwargs
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_scatter_plot(data, x, y, color_by=None, title="", **kwargs):
    """Create a scatter plot"""
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color_by,
        title=title,
        trendline="ols" if kwargs.get('show_trendline', False) else None,
        **{k: v for k, v in kwargs.items() if k != 'show_trendline'}
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_box_plot(data, x, y, color_by=None, title="", **kwargs):
    """Create a box plot"""
    # Remove show_trendline if present (not applicable to box plots)
    kwargs = {k: v for k, v in kwargs.items() if k != 'show_trendline'}
    
    fig = px.box(
        data,
        x=x,
        y=y,
        color=color_by,
        title=title,
        points='outliers',
        **kwargs
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_violin_plot(data, x, y, color_by=None, title="", **kwargs):
    """Create a violin plot"""
    # Remove show_trendline if present (not applicable to violin plots)
    kwargs = {k: v for k, v in kwargs.items() if k != 'show_trendline'}
    
    fig = px.violin(
        data,
        x=x,
        y=y,
        color=color_by,
        title=title,
        box=True,
        points='outliers',
        **kwargs
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_area_chart(data, x, y, color_by=None, title="", **kwargs):
    """Create an area chart"""
    # Remove show_trendline if present (not applicable to area charts)
    kwargs = {k: v for k, v in kwargs.items() if k != 'show_trendline'}
    
    fig = px.area(
        data,
        x=x,
        y=y,
        color=color_by,
        title=title,
        **kwargs
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_histogram(data, x, color_by=None, title="", **kwargs):
    """Create a histogram"""
    # Remove show_trendline if present (not applicable to histograms)
    kwargs = {k: v for k, v in kwargs.items() if k != 'show_trendline'}
    
    # For histograms, we need a numeric column, not date
    # If x is 'date', we should skip it and show an error or use a different column
    if x == 'date' or 'date' in str(x).lower():
        # Create an error message figure
        fig = go.Figure()
        fig.add_annotation(
            text="⚠️ Histograms require a numeric metric, not dates.<br>Please select a numeric column like 'minutesAsleep', 'steps', etc.",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="orange"),
            align="center"
        )
        fig.update_layout(
            height=500,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    # Auto-detect participant column if not specified
    if not color_by or color_by not in data.columns:
        if 'participant' in data.columns:
            color_by = 'participant'
        elif 'participantId' in data.columns:
            color_by = 'participantId'
        elif 'participant_type' in data.columns and data['participant_type'].nunique() > 1:
            color_by = 'participant_type'
        else:
            color_by = None
    
    fig = px.histogram(
        data,
        x=x,
        color=color_by,
        title=title,
        marginal='box',
        nbins=30,
        barmode='overlay',
        opacity=0.7,
        **kwargs
    )
    
    fig.update_layout(
        height=500,
        showlegend=True if color_by else False,
        xaxis_title=x,
        yaxis_title='Count'
    )
    
    return fig

def create_heatmap(data, x, y, values, title="", **kwargs):
    """Create a heatmap (calendar-style)"""
    # Pivot data for heatmap
    pivot_data = data.pivot_table(
        values=values,
        index=data[y].dt.isocalendar().week if hasattr(data[y], 'dt') else y,
        columns=data[x].dt.dayofweek if hasattr(data[x], 'dt') else x,
        aggfunc='mean'
    )
    
    fig = px.imshow(
        pivot_data,
        title=title,
        labels=dict(x="Day of Week", y="Week", color=values),
        color_continuous_scale='Viridis',
        **kwargs
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_custom_chart(chart_config):
    """
    Create a chart based on configuration dictionary
    
    Args:
        chart_config (dict): Configuration with keys:
            - type: chart type (line_chart, bar_chart, etc.)
            - data: pandas DataFrame
            - x: x-axis column
            - y: y-axis column or list of columns
            - color_by: column to color by
            - title: chart title
            - other kwargs
    """
    chart_type = chart_config.get('type', 'line_chart')
    data = chart_config.get('data')
    x = chart_config.get('x')
    y = chart_config.get('y')
    color_by = chart_config.get('color_by')
    title = chart_config.get('title', '')
    
    # Remove used keys from config to pass rest as kwargs
    kwargs = {k: v for k, v in chart_config.items() 
              if k not in ['type', 'data', 'x', 'y', 'color_by', 'title']}
    
    # Map chart types to functions
    chart_functions = {
        'line_chart': create_line_chart,
        'bar_chart': create_bar_chart,
        'scatter_plot': create_scatter_plot,
        'box_plot': create_box_plot,
        'violin_plot': create_violin_plot,
        'area_chart': create_area_chart,
        'histogram': create_histogram,
    }
    
    chart_func = chart_functions.get(chart_type, create_line_chart)
    
    try:
        if chart_type == 'histogram':
            return chart_func(data, x, color_by, title, **kwargs)
        else:
            return chart_func(data, x, y, color_by, title, **kwargs)
    except Exception as e:
        # Return an error figure
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="red")
        )
        return fig

def apply_custom_styling(fig, config):
    """Apply custom styling to a figure"""
    if 'colors' in config and config['colors']:
        fig.update_traces(marker=dict(color=config['colors'][0]))
    
    if 'show_grid' in config:
        fig.update_xaxes(showgrid=config['show_grid'])
        fig.update_yaxes(showgrid=config['show_grid'])
    
    if 'x_label' in config:
        fig.update_xaxes(title_text=config['x_label'])
    
    if 'y_label' in config:
        fig.update_yaxes(title_text=config['y_label'])
    
    return fig

