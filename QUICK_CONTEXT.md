# ⚡ Quick Context - OCD Fitbit Analysis Platform

**Use this for quick AI assistant context. For full details, see PROJECT_CONTEXT.md**

---

## 🎯 What This Is
Streamlit app for comparing OCD vs Control participants using Fitbit data. Built for non-technical research assistants.

## 🏗️ Tech Stack
- **Framework:** Streamlit (Python-only)
- **Charts:** Plotly
- **Stats:** SciPy, Pandas
- **AI (Current):** Hardcoded responses (dummy)
- **Data (Current):** Sample data generator
- **AI (Future):** Claude API
- **Data (Future):** AWS S3

## 📁 Key Files
```
streamlit_app/
├── app.py                      # Main entry
├── pages/
│   ├── 1_🤖_Quick_Analysis.py  # Automated
│   ├── 2_🎯_Guided_Analysis.py # Assisted
│   └── 3_⚙️_Custom_Analysis.py # Manual
├── utils/
│   ├── data_loader.py          # Sample data
│   ├── ai_assistant.py         # Dummy AI
│   ├── chart_factory.py        # Plotly charts
│   └── statistical_analysis.py # T-tests, etc.
└── config/settings.py          # All configuration
```

## 🎨 Three Modes
1. **Quick AI:** One-click automated analysis
2. **Guided:** Step-by-step with AI suggestions
3. **Custom:** Full manual control

## 🔑 Key Decisions

### Why Streamlit?
Fast development, Python-only, research-friendly

### Why Dummy AI?
Zero cost during dev, easy to migrate to real API later

### Why Sample Data?
No AWS dependency, faster iteration

### Why Three Modes?
Serve users from beginner to expert

## 📊 Data Structure
```python
data = pd.DataFrame({
    'date': datetime,
    'participantId': str,
    'participant_type': str,  # "OCD" or "Control"
    'minutesAsleep': int,
    'steps': int,
    # ... any Fitbit metric
})
```

## 🎯 Design Principles
1. **Metric-agnostic** - Works with ANY Fitbit metric
2. **Configuration-driven** - Settings in config/settings.py
3. **Progressive complexity** - Easy → Advanced modes
4. **Component reusability** - DRY principle

## 🚀 How to Run
```bash
cd streamlit_app
./run.sh
```

## 📝 Common Tasks

### Add New Metric
1. Edit `config/settings.py` - add to AVAILABLE_METRICS
2. Edit `utils/data_loader.py` - generate sample data
3. Done! Everything else automatic

### Migrate to Real AI
Replace in `utils/ai_assistant.py`:
```python
# Current
def generate_ai_insights(data):
    return "hardcoded response..."

# Future
def generate_ai_insights(data):
    client = anthropic.Anthropic(api_key=KEY)
    return client.messages.create(...)
```

### Migrate to S3
Replace in `utils/data_loader.py`:
```python
# Current
data = generate_sample_data()

# Future
data = pd.read_csv(f"s3://bucket/{id}/data.csv")
```

## ✅ Current Status
**Phase:** MVP Complete  
**Works:** All 3 modes, charts, stats, dummy AI, sample data  
**Next:** AWS S3 + Real AI integration

## 🎓 Key Insights
- System is **metric-agnostic** (not hardcoded for sleep)
- Add metrics in config, everything else works
- Architecture supports 40+ Fitbit metrics
- Easy to extend and maintain

## 📚 Full Documentation
- **PROJECT_CONTEXT.md** - Complete context (this summary is from there)
- **README.md** - Technical docs
- **QUICK_START.md** - User guide
- **ADDING_NEW_METRICS.md** - Metric guide

---

**For AI Assistants:** Read PROJECT_CONTEXT.md for complete details. This is just a quick reference.

