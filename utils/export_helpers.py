"""
Export functionality for charts and data
"""
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

def export_chart_as_png(fig, filename=None):
    """
    Export Plotly figure as PNG
    Returns bytes buffer for download
    """
    if filename is None:
        filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    # Convert to PNG bytes
    img_bytes = fig.to_image(format="png", width=1200, height=800)
    
    return img_bytes, filename

def export_chart_as_pdf(fig, filename=None):
    """
    Export Plotly figure as PDF
    Returns bytes buffer for download
    """
    if filename is None:
        filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Convert to PDF bytes
    pdf_bytes = fig.to_image(format="pdf", width=1200, height=800)
    
    return pdf_bytes, filename

def export_chart_as_html(fig, filename=None):
    """
    Export Plotly figure as interactive HTML
    Returns HTML string for download
    """
    if filename is None:
        filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    # Convert to HTML
    html_string = fig.to_html(include_plotlyjs='cdn')
    
    return html_string, filename

def export_data_as_csv(data, filename=None):
    """
    Export DataFrame as CSV
    Returns CSV string for download
    """
    if filename is None:
        filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Convert to CSV
    csv_string = data.to_csv(index=False)
    
    return csv_string, filename

def export_data_as_excel(data, filename=None):
    """
    Export DataFrame as Excel
    Returns bytes buffer for download
    """
    if filename is None:
        filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Convert to Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Data')
    
    excel_bytes = output.getvalue()
    
    return excel_bytes, filename

def create_filename(chart_title, extension, participant_ids=None):
    """
    Create a descriptive filename for exports
    
    Args:
        chart_title: Title of the chart
        extension: File extension (png, pdf, csv, etc.)
        participant_ids: List of participant IDs (optional)
    
    Returns:
        Formatted filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Sanitize chart title for filename
    safe_title = chart_title.replace(' ', '_').replace(':', '').replace('/', '_')
    safe_title = ''.join(c for c in safe_title if c.isalnum() or c == '_')[:50]
    
    if participant_ids and len(participant_ids) <= 3:
        # Include participant IDs if not too many
        participants_str = '_'.join(participant_ids)
        filename = f"{safe_title}_{participants_str}_{timestamp}.{extension}"
    else:
        filename = f"{safe_title}_{timestamp}.{extension}"
    
    return filename

