# 📥 Export Functionality Guide

Complete guide to exporting charts and data from the OCD Fitbit Analysis Platform.

---

## 🎯 Overview

All three analysis modes (Quick AI, Guided, Custom) support comprehensive export functionality:

- **📊 CSV** - Raw data export for further analysis
- **📥 PNG** - High-resolution chart images (1200x800px)
- **📄 PDF** - Publication-quality vector graphics

---

## 🚀 Quick Start

### Using Export Buttons

After generating any chart in the app:

1. **Locate the export buttons** below the chart
2. **Choose your format:**
   - Click **📊 CSV** to download data
   - Click **📥 PNG** to download chart as image
   - Click **📄 PDF** to download chart as PDF
3. **File downloads automatically** with descriptive filename

That's it! Your export is ready to use.

---

## 📊 Export Formats

### 1. CSV Data Export

**Best for:**
- Further analysis in Excel, R, Python, SPSS
- Sharing raw data with colleagues
- Creating custom visualizations elsewhere
- Statistical analysis in other tools

**What's included:**
- All selected participants
- All metrics in the current view
- Date ranges as configured
- Clean, ready-to-use format

**Example filename:**
```
Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143022.csv
```

**Format:**
```csv
date,participant,minutesAsleep,efficiency,steps
2023-06-01,BKQ3HJ,395,82.0,8234
2023-06-01,BRT57L,425,87.5,10523
...
```

### 2. PNG Image Export

**Best for:**
- PowerPoint presentations
- Posters and infographics
- Web publishing
- Quick sharing via email/Slack

**Specifications:**
- Resolution: 1200 x 800 pixels
- High DPI for sharp text
- Transparent background option
- Optimized file size

**Example filename:**
```
Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143022.png
```

**File size:** Typically 50-150 KB

### 3. PDF Document Export

**Best for:**
- Academic publications
- Formal reports
- Print materials
- Vector graphics (scalable)

**Specifications:**
- Vector format (scales perfectly)
- 1200 x 800 point size
- Embedded fonts
- High-quality rendering

**Example filename:**
```
Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143022.pdf
```

**File size:** Typically 20-50 KB

---

## 🎨 Export in Each Mode

### Quick AI Analysis Mode

**Location:** Below each suggested visualization

**Features:**
- Export all AI-generated charts
- Separate exports for each chart type
- Data export includes all analyzed metrics

**Workflow:**
```
1. Run Smart Analysis
2. View charts in "Visualizations" tab
3. Click export button below desired chart
4. File downloads automatically
```

### Guided Analysis Mode

**Location:** Below each generated chart in Step 4

**Features:**
- Export selected charts only
- Include/exclude charts before export
- Customized data based on your selections

**Workflow:**
```
1. Complete Steps 1-3
2. Generate charts in Step 4
3. Review charts
4. Export individual charts as needed
```

### Custom Analysis Mode

**Location:** In the action buttons row (top-right of chart area)

**Features:**
- Full control over what gets exported
- Export exactly what you see
- Real-time preview before export

**Workflow:**
```
1. Configure your chart
2. Preview in main area
3. Click export buttons
4. Choose format
```

---

## 🔧 Advanced Features

### Intelligent Filename Generation

Filenames are automatically generated with:

1. **Chart title** (sanitized, max 50 chars)
2. **Participant IDs** (up to 3 participants)
3. **Timestamp** (YYYYMMDD_HHMMSS)

**Example transformations:**
```
Chart Title: "Sleep Efficiency: OCD vs Control"
Participants: BKQ3HJ, BRT57L
Timestamp: 2023-10-09 14:30:22

Result: Sleep_Efficiency_OCD_vs_Control_BKQ3HJ_BRT57L_20231009_143022.png
```

### Batch Export (Coming Soon)

Future feature to export multiple charts at once:
- Select multiple charts
- Export all in one click
- Choose ZIP or individual downloads
- Preserve folder structure

### Custom Export Settings (Coming Soon)

Future customization options:
- Image resolution (DPI)
- Image dimensions
- Background color
- Font sizes
- File format options

---

## 💡 Best Practices

### For Presentations

✅ **Do:**
- Use PNG format
- Export at standard resolution
- Include descriptive chart titles
- Use clear color schemes

❌ **Don't:**
- Over-compress images
- Use charts without titles
- Export cluttered visualizations

### For Publications

✅ **Do:**
- Use PDF format for vector graphics
- Ensure axes are clearly labeled
- Use professional color palettes
- Include statistical annotations

❌ **Don't:**
- Use PNG when scaling is needed
- Export without proper labels
- Use low-contrast colors

### For Data Sharing

✅ **Do:**
- Export CSV with all relevant metrics
- Include date ranges in filename
- Document participant information
- Verify data completeness

❌ **Don't:**
- Share data without context
- Export incomplete date ranges
- Forget participant privacy considerations

---

## 🐛 Troubleshooting

### Problem: "PNG export requires 'kaleido' package"

**Cause:** The kaleido library is not installed

**Solution:**
```bash
pip install kaleido
```

**Verification:**
```bash
python -c "import kaleido; print('Kaleido installed!')"
```

### Problem: "PDF export failed"

**Cause:** Same as PNG - missing kaleido

**Solution:**
```bash
pip install kaleido==0.2.1
```

### Problem: CSV export is empty

**Cause:** No data in current view

**Solution:**
1. Check participant selection
2. Verify date range
3. Ensure metrics are selected
4. Try regenerating the chart

### Problem: Filename is too long

**Cause:** Too many participants or long chart title

**Solution:**
- System automatically truncates long names
- Chart titles limited to 50 characters
- Max 3 participant IDs in filename

### Problem: Export button not visible

**Cause:** Chart not fully rendered

**Solution:**
1. Wait for chart to load completely
2. Scroll down to see export buttons
3. Refresh the page if needed

---

## 📊 Export File Structure

### Single Export

When exporting individual charts:

```
Downloads/
└── Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143022.png
```

### Multiple Exports from Same Session

Timestamps ensure unique filenames:

```
Downloads/
├── Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143022.png
├── Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143045.png
└── Steps_Analysis_BKQ3HJ_BRT57L_20231009_143102.csv
```

---

## 🔒 Privacy & Security

### Data Handling

- **No server storage**: Exports happen client-side
- **No tracking**: Export actions are not logged
- **Privacy-first**: Participant IDs in filenames are your responsibility

### Recommendations

✅ **Do:**
- Review filenames before sharing
- Store exports in secure locations
- Follow your institution's data policies
- Anonymize data when required

❌ **Don't:**
- Share exports publicly without review
- Store exports in unsecured cloud folders
- Include identifying information unnecessarily

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Batch export** - Export multiple charts at once
- [ ] **Custom resolutions** - Choose image size
- [ ] **Excel format** - Multi-sheet Excel exports
- [ ] **Interactive HTML** - Self-contained interactive charts
- [ ] **Report builder** - Combine multiple exports
- [ ] **Cloud save** - Direct save to cloud storage
- [ ] **Email integration** - Email exports directly
- [ ] **Scheduled exports** - Automated regular exports

---

## 📖 Related Documentation

- **Main README:** [README.md](README.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **Project Context:** [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)
- **Adding Metrics:** [ADDING_NEW_METRICS.md](ADDING_NEW_METRICS.md)

---

## 🛠️ Technical Details

### Implementation

Export functionality is implemented in `utils/export_helpers.py`:

```python
from utils.export_helpers import (
    export_chart_as_png,     # PNG export
    export_chart_as_pdf,     # PDF export
    export_data_as_csv,      # CSV export
    create_filename          # Smart filename generation
)
```

### Dependencies

- **kaleido** (0.2.1) - PNG/PDF chart rendering
- **openpyxl** (3.1.2) - Excel support (future)
- **plotly** (5.18.0) - Built-in export methods
- **pandas** (2.0.3) - CSV generation

### Code Example

```python
# Export PNG
img_bytes, filename = export_chart_as_png(
    fig,
    create_filename("My Chart", "png", ["BKQ3HJ", "BRT57L"])
)

# Export PDF
pdf_bytes, filename = export_chart_as_pdf(fig)

# Export CSV
csv_data, filename = export_data_as_csv(dataframe)
```

---

## ✨ Summary

Export functionality is:
- ✅ **Available in all modes**
- ✅ **Three formats supported** (CSV, PNG, PDF)
- ✅ **Automatic filename generation**
- ✅ **High-quality outputs**
- ✅ **Easy to use**
- ✅ **No manual file management needed**

**Happy exporting! 📥**

