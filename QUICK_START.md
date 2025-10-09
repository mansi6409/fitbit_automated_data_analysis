# 🚀 Quick Start Guide

## Installation & Running (3 Easy Steps)

### Option 1: Using the Run Script (Easiest)

```bash
cd streamlit_app
./run.sh
```

That's it! The script will:
- Create a virtual environment
- Install all dependencies
- Launch the app in your browser

### Option 2: Manual Installation

**Step 1: Navigate to directory**
```bash
cd /Users/mansigarg/USC/LAB/ocd-research-app/dataanalysis/streamlit_app
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## First Time Using the App?

### 🎯 Recommended Flow for Beginners

1. **Start with Quick Analysis** 
   - Click "Start Quick Analysis" on the home page
   - Select PAIR001 from the participant list
   - Click "Run Smart Analysis"
   - Explore the AI insights, charts, and statistics

2. **Try Guided Analysis**
   - Navigate to "Guided Analysis"
   - Follow the 4-step wizard
   - See how AI suggestions work
   - Customize as needed

3. **Explore Custom Analysis**
   - Go to "Custom Analysis"
   - Play with different chart types
   - Customize colors and styling
   - Export your data

---

## What Each Mode Does

### 🤖 Quick AI Analysis
**Best for:** Quick insights, first-time users, busy researchers

**What it does:**
- Automatically generates insights
- Creates recommended visualizations
- Runs statistical tests
- Detects anomalies

**How to use:**
1. Select participants (try selecting a pair)
2. Click "Run Smart Analysis"
3. View results in 4 tabs: Insights, Visualizations, Statistics, Anomalies

### 🎯 Guided Analysis
**Best for:** Most research tasks, balanced workflow

**What it does:**
- Step-by-step workflow
- AI suggests options
- You choose what to include
- Generate final analysis

**How to use:**
1. **Step 1:** Select participants
2. **Step 2:** Choose metrics (AI suggests relevant ones)
3. **Step 3:** Pick visualizations (include/exclude suggested charts)
4. **Step 4:** View and export results

### ⚙️ Custom Analysis
**Best for:** Expert users, specific visualization needs

**What it does:**
- Full manual control
- Customize every aspect
- Advanced statistical analysis
- Real-time preview

**How to use:**
1. Configure data selection in sidebar
2. Choose chart type and metrics
3. Customize styling
4. View live preview
5. Run additional analysis
6. Export results (PNG, PDF, or CSV)

---

## 📥 Exporting Your Work

All three modes support easy data and chart export:

### Export Formats

**1. PNG Images (1200x800px)**
- Click **📥 PNG** button below any chart
- High-resolution images for presentations
- Ideal for PowerPoint, posters, reports

**2. PDF Documents**
- Click **📄 PDF** button below any chart
- Publication-quality vector graphics
- Perfect for papers and formal reports

**3. CSV Data Files**
- Click **📊 CSV** button to download raw data
- All selected metrics and date ranges included
- Ready for Excel, R, SPSS, or other tools

### Export Filenames

Filenames automatically include:
- Chart title (sanitized)
- Participant IDs (up to 3)
- Timestamp (YYYYMMDD_HHMMSS)

**Example:** `Sleep_Efficiency_BKQ3HJ_BRT57L_20231009_143530.png`

### Troubleshooting Export

If PNG/PDF export shows an error:
```bash
pip install kaleido
```

CSV export always works without additional dependencies.

---

## Sample Workflows

### Workflow 1: Compare OCD vs Control Sleep Patterns

```
1. Open Quick Analysis
2. Select PAIR001 (BKQ3HJ ↔ BRT57L)
3. Click "Run Smart Analysis"
4. Review:
   - AI Insights tab → Read the summary
   - Visualizations tab → See sleep trends
   - Statistical Tests tab → Check p-values
   - Anomalies tab → Look for unusual patterns
```

### Workflow 2: Build Custom Correlation Chart

```
1. Open Custom Analysis
2. Select 2+ participants
3. Chart type → Scatter Plot
4. X-Axis → minutesAsleep
5. Y-Axis → steps
6. Color by → Participant Type
7. View correlation in real-time
8. Export as needed
```

### Workflow 3: Weekly Pattern Analysis

```
1. Open Guided Analysis
2. Select participants
3. Choose metrics: sleep, steps, heart_rate
4. Include "Weekly Activity Patterns" heatmap
5. Generate analysis
6. Use AI insights to interpret patterns
```

---

## Understanding the Data

### Current Data Source
The app uses **simulated sample data** that mimics real Fitbit data patterns:

- **OCD Participants:** Typically show reduced sleep duration, lower efficiency
- **Control Participants:** More consistent sleep patterns, higher activity
- **Date Range:** June 1 - August 31, 2023 (92 days)
- **Metrics:** Sleep, activity, heart rate

### Available Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| Minutes Asleep | Total sleep duration | minutes |
| Sleep Efficiency | Sleep quality percentage | % |
| Time in Bed | Total time spent in bed | minutes |
| Minutes Awake | Time awake during sleep period | minutes |
| Steps | Daily step count | steps |
| Heart Rate | Resting heart rate | BPM |
| Calories | Calories burned | kcal |

### Participant Pairs

| Pair ID | OCD Participant | Control Participant |
|---------|----------------|---------------------|
| PAIR001 | BKQ3HJ | BRT57L |
| PAIR002 | BWPTFS | BWY5LB |
| PAIR003 | BX8KLH | BX8NTV |
| PAIR004 | BXMMHR | BYG334 |
| PAIR005 | BZCKBJ | C227P4 |

---

## Tips for Best Results

### ✅ Do's

- **Compare pairs:** Always compare OCD with matched controls
- **Check date ranges:** Ensure you're comparing comparable time periods
- **Use multiple visualizations:** Different charts reveal different patterns
- **Read AI suggestions:** Even in custom mode, AI can provide helpful tips
- **Explore all tabs:** Don't miss anomalies and statistics

### ❌ Don'ts

- **Don't compare incompatible date ranges:** Ensure overlap
- **Don't ignore data quality warnings:** Missing data affects results
- **Don't rely on single chart type:** Use multiple views
- **Don't skip statistical tests:** Numbers matter as much as visuals

---

## Troubleshooting

### Problem: "No data found"
**Solution:** 
- Check that participants are selected
- Verify date range if using custom dates
- Try selecting a different participant

### Problem: Charts not loading
**Solution:**
- Refresh the page (Ctrl+R)
- Check browser console for errors
- Ensure all dependencies are installed
- Try a different chart type

### Problem: App won't start
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Restart app
streamlit run app.py
```

### Problem: Slow performance
**Solution:**
- Reduce number of participants
- Use shorter date range
- Clear browser cache
- Restart the app

---

## Keyboard Shortcuts

When using the app:

| Shortcut | Action |
|----------|--------|
| `Ctrl+R` | Refresh page |
| `C` | Clear cache |
| `R` | Rerun app |

---

## Next Steps

1. **Familiarize yourself** with all three modes
2. **Try different participant combinations**
3. **Experiment with chart types**
4. **Read the full README.md** for detailed documentation
5. **Start analyzing your research questions!**

---

## Getting Help

- **Documentation:** See README.md
- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Docs:** https://plotly.com/python/

---

**Happy Analyzing! 🔬📊**

