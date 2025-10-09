# 🔬 OCD Fitbit Data Analysis Platform

A comprehensive Streamlit-based platform for analyzing Fitbit data comparing OCD participants with healthy controls.

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip or conda

### Installation

1. **Navigate to the streamlit_app directory:**
```bash
cd streamlit_app
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
streamlit_app/
├── app.py                          # Main entry point
├── pages/                          # Streamlit pages
│   ├── 1_🤖_Quick_Analysis.py      # AI-powered quick analysis
│   ├── 2_🎯_Guided_Analysis.py     # AI-assisted guided workflow
│   └── 3_⚙️_Custom_Analysis.py     # Full manual control
├── components/                     # Reusable UI components
│   └── participant_selector.py    # Participant selection widget
├── utils/                          # Utility functions
│   ├── data_loader.py             # Data loading (uses sample data)
│   ├── ai_assistant.py            # AI insights (dummy responses)
│   ├── statistical_analysis.py    # Statistical tests
│   └── chart_factory.py           # Plotly chart creation
├── config/
│   └── settings.py                # Configuration settings
└── requirements.txt               # Python dependencies
```

## 🎯 Features

### Three Analysis Modes

1. **🤖 Quick AI Analysis**
   - One-click automated analysis
   - AI-generated insights (hardcoded for now)
   - Automatic visualization suggestions
   - Statistical comparisons
   - Anomaly detection

2. **🎯 Guided Analysis**
   - Step-by-step workflow
   - AI suggestions with user control
   - Recommended metrics and charts
   - Interactive chart selection

3. **⚙️ Custom Analysis**
   - Full manual control
   - Complete chart customization
   - Advanced statistical analysis
   - Export capabilities

### Key Capabilities

- **Participant Management**: Easy selection of OCD and Control participants
- **Multiple Visualizations**: Line, bar, scatter, box, violin, area charts, histograms
- **Statistical Analysis**: T-tests, correlations, effect sizes
- **AI Insights**: Automated pattern detection and recommendations
- **Data Export**: 
  - 📊 **CSV** - Export raw data in CSV format
  - 📥 **PNG** - Export charts as high-resolution PNG images (1200x800)
  - 📄 **PDF** - Export charts as PDF for publications
  - 📱 **Interactive HTML** - Save interactive charts (coming soon)

## 📊 Current Data Source

The app currently uses **sample data** generated programmatically. The data simulates:
- Sleep metrics (duration, efficiency, time in bed)
- Activity metrics (steps, calories)
- Heart rate data
- Realistic patterns for OCD vs Control groups

**Note:** AWS S3 integration and real data loading will be added in future iterations.

## 🤖 AI Features (Current Implementation)

The AI assistant currently uses **hardcoded responses** to simulate LLM behavior:

- `generate_ai_insights()` - Returns pre-written insights based on data patterns
- `suggest_visualizations()` - Rule-based chart recommendations
- `detect_anomalies()` - Statistical anomaly detection
- `generate_comparison_insights()` - OCD vs Control comparison summaries

**Future:** Will integrate with Claude API or OpenAI GPT for real AI-powered insights.

## 🔧 Configuration

Edit `config/settings.py` to customize:
- Participant pairs (OCD-Control matching)
- Available metrics
- Chart types
- Color palettes
- Statistical thresholds

## 📝 Usage Examples

### Example 1: Quick Comparison
1. Open the app
2. Click "Start Quick Analysis"
3. Select a matched pair (e.g., PAIR001)
4. Click "Run Smart Analysis"
5. View AI insights, charts, statistics, and anomalies

### Example 2: Custom Visualization
1. Navigate to "Custom Analysis"
2. Select participants from the sidebar
3. Choose chart type and metrics
4. Customize colors and styling
5. Export or analyze further

### Example 3: Guided Workflow
1. Go to "Guided Analysis"
2. Follow the step-by-step process
3. AI suggests options at each step
4. Accept or modify suggestions
5. Generate final analysis

### Exporting Your Work

All three analysis modes support exporting:

**📥 Export Charts (PNG/PDF):**
- Click the **PNG** or **PDF** button below any chart
- Charts are exported at 1200x800px resolution
- Filenames include chart title, participant IDs, and timestamp
- Example: `Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143022.png`

**📊 Export Data (CSV):**
- Click the **CSV** button to download the underlying data
- Data includes all selected metrics and date ranges
- Perfect for further analysis in Excel or statistical software

**💡 Tip:** If PNG/PDF export fails, ensure `kaleido` is installed:
```bash
pip install kaleido
```

## 🛠️ Development

### Adding New Features

**New Chart Type:**
1. Add chart type to `config/settings.py`
2. Implement chart function in `utils/chart_factory.py`
3. Update chart type mapping in custom analysis

**New Metric:**
1. Add to `AVAILABLE_METRICS` in `config/settings.py`
2. Add display name to `METRIC_LABELS`
3. Update data loader if needed

**New AI Insight:**
1. Add function to `utils/ai_assistant.py`
2. Return hardcoded response based on data patterns
3. Call from appropriate page

### Testing

```bash
# Run the app in debug mode
streamlit run app.py --logger.level=debug

# Check for errors in terminal output
```

## 📦 Dependencies

Main packages:
- `streamlit` - Web app framework
- `plotly` - Interactive visualizations
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scipy` - Statistical analysis
- `ydata-profiling` - Automated profiling

See `requirements.txt` for complete list.

## 🚧 Roadmap

### Phase 1: Current (Sample Data + Dummy AI) ✅
- [x] Sample data generation
- [x] Three analysis modes
- [x] Participant selection
- [x] Basic visualizations
- [x] Hardcoded AI responses
- [x] Statistical analysis
- [x] Export functionality (PNG, PDF, CSV)

### Phase 2: Real Data Integration
- [ ] AWS S3 connection
- [ ] Load actual participant data
- [ ] Data validation and cleaning
- [ ] Error handling

### Phase 3: Real AI Integration
- [ ] Claude/OpenAI API integration
- [ ] Dynamic insight generation
- [ ] Cost-optimized API usage
- [ ] Caching for performance

### Phase 4: Advanced Features
- [ ] Export to PNG/PDF
- [ ] Report generation
- [ ] Saved configurations
- [ ] Multi-user support
- [ ] Deployment to cloud

## 🐛 Troubleshooting

**Issue:** Charts not displaying
- **Solution:** Check that data is loaded correctly, try reselecting participants

**Issue:** Import errors
- **Solution:** Ensure you're in the `streamlit_app` directory and all dependencies are installed

**Issue:** "No data found"
- **Solution:** Data generator creates sample data automatically - check console for errors

## 💡 Tips

- Start with **Quick Analysis** to understand the platform
- Use **Guided Analysis** for most research tasks
- Reserve **Custom Analysis** for specific, complex visualizations
- Compare OCD vs Control participants for best statistical insights
- Check AI suggestions even when using manual mode

## 📧 Support

For questions or issues:
1. Check this README
2. Review the code comments
3. Check Streamlit documentation: https://docs.streamlit.io

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ using Streamlit, Plotly, and Python**

