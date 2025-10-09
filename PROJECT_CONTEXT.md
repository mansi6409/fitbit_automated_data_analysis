# 🔬 OCD Fitbit Analysis Platform - Project Context Document

**Purpose:** This document provides complete context about the project, architecture decisions, and implementation details for future AI assistant conversations.

**Last Updated:** 2024-10-09  
**Project Status:** MVP Complete - Sample Data + Dummy AI  
**Next Phase:** AWS S3 Integration + Real AI

---

## 📋 PROJECT OVERVIEW

### What This Is
A **Streamlit-based data analysis platform** for comparing OCD participants with healthy controls using Fitbit wearable data. Built for research assistants (non-technical users) in an OCD research lab.

### Primary Use Case
- **Users:** Research assistants (RAs) with limited CS background but strong analysis skills
- **Data:** Fitbit wearable data (sleep, activity, heart rate, etc.)
- **Goal:** Compare OCD participants vs matched healthy controls
- **Pairing:** Each OCD participant is matched 1:1 with a control participant

### Key Requirements
1. **Easy to use** - RAs are not programmers
2. **Flexible analysis** - Both automated and manual modes
3. **Cost-effective** - Minimize AWS costs
4. **Automated** - AI-assisted insights and suggestions
5. **Robust** - Handle real research data reliably

---

## 🏗️ ARCHITECTURE DECISIONS

### Technology Stack (FINAL)

```yaml
Framework: Streamlit (Python-only, no JavaScript)
Visualization: Plotly (interactive charts)
Data Processing: Pandas, NumPy
Statistics: SciPy
AI (Current): Hardcoded responses (dummy implementation)
AI (Future): Claude API (Anthropic) or OpenAI GPT
Data Source (Current): Sample data generator
Data Source (Future): AWS S3 bucket
Database (Future): PostgreSQL for processed data (optional)
Deployment (Future): Streamlit Community Cloud or AWS
```

### Why Streamlit?
✅ **Python-only** - No JavaScript/React complexity  
✅ **Fast development** - Build in days, not weeks  
✅ **Research-friendly** - Familiar to data scientists  
✅ **Built-in widgets** - No UI framework needed  
✅ **Easy deployment** - Streamlit Cloud is free  
✅ **Interactive by default** - Perfect for data exploration  

**Rejected Alternatives:**
- ❌ React + Flask: Too complex, two codebases
- ❌ Dash: More verbose than Streamlit
- ❌ Jupyter Notebooks: Not suitable for end users

### Why Three Analysis Modes?
We implemented **progressive complexity** to serve different user needs:

1. **🤖 Quick AI Analysis** (Beginner)
   - One-click automated analysis
   - AI does everything
   - Best for: Quick insights, first-time users

2. **🎯 Guided Analysis** (Intermediate)
   - Step-by-step wizard
   - AI suggests, user chooses
   - Best for: Most research tasks, balanced control

3. **⚙️ Custom Analysis** (Expert)
   - Full manual control
   - Complete customization
   - Best for: Specific analyses, expert users

**Rationale:** Users can start simple and grow into complexity as they learn.

### Why Dummy AI Now?
✅ **Faster development** - No API setup during prototyping  
✅ **Zero cost** - No API charges while testing  
✅ **Predictable** - Easier debugging  
✅ **Easy migration** - Just swap function implementation later  

**Implementation:**
- Hardcoded responses in `utils/ai_assistant.py`
- Realistic narratives based on data patterns
- Simulates LLM without API calls
- Will replace with Claude API (cheap, high-quality)

### Why Sample Data Now?
✅ **No AWS dependency** - Can develop/test locally  
✅ **Realistic patterns** - Different for OCD vs Control  
✅ **Controlled testing** - Known data characteristics  
✅ **Fast iteration** - No S3 latency  

**Implementation:**
- Programmatic data generation in `utils/data_loader.py`
- 92 days of data per participant
- Realistic noise and missing values
- Easy to swap with real S3 data later

---

## 📁 PROJECT STRUCTURE

```
streamlit_app/
├── app.py                          # Main entry point & home page
│
├── pages/                          # Streamlit multi-page app
│   ├── 1_🤖_Quick_Analysis.py      # Automated AI analysis
│   ├── 2_🎯_Guided_Analysis.py     # Step-by-step workflow
│   └── 3_⚙️_Custom_Analysis.py     # Full manual control
│
├── components/                     # Reusable UI components
│   └── participant_selector.py     # Participant selection widget
│
├── utils/                          # Core functionality
│   ├── data_loader.py              # Sample data generation
│   ├── ai_assistant.py             # Dummy AI (hardcoded)
│   ├── statistical_analysis.py     # T-tests, correlations
│   └── chart_factory.py            # Plotly chart creation
│
├── config/
│   └── settings.py                 # Configuration & constants
│
├── requirements.txt                # Python dependencies
├── run.sh                          # Quick start script
│
└── Documentation/
    ├── README.md                   # Complete technical docs
    ├── QUICK_START.md              # User guide
    ├── PROJECT_SUMMARY.md          # High-level overview
    ├── ADDING_NEW_METRICS.md       # How to add metrics
    └── PROJECT_CONTEXT.md          # This file
```

---

## 🎯 KEY DESIGN PATTERNS

### 1. Configuration-Driven Architecture

**Pattern:** All metrics, pairs, settings in `config/settings.py`

```python
AVAILABLE_METRICS = ["minutesAsleep", "steps", "heart_rate", ...]
PARTICIPANT_PAIRS = {"PAIR001": {"ocd": "BKQ3HJ", "control": "BRT57L"}, ...}
```

**Benefit:** Add new metrics/participants without code changes

### 2. Metric-Agnostic Design

**Pattern:** No hardcoded metric names in logic

```python
# Generic - works with ANY metric
def create_line_chart(data, x, y, ...):
    fig = px.line(data, x=x, y=y, ...)
```

**Benefit:** System works with ALL Fitbit metrics, not just sleep

### 3. Component Reusability

**Pattern:** Reusable UI components

```python
# Used in all three modes
selected = participant_selector(mode="mixed", key_prefix="quick")
```

**Benefit:** Consistent UX, less code duplication

### 4. Dummy Implementation Pattern

**Pattern:** Hardcoded responses that simulate real AI

```python
def generate_ai_insights(data):
    # Returns realistic hardcoded text based on data patterns
    # Will replace with: client.messages.create(model="claude-3-haiku", ...)
```

**Benefit:** Develop full workflow without API dependencies

### 5. Progressive Enhancement

**Pattern:** Start simple, add complexity later

- Phase 1: Sample data + Dummy AI ✅
- Phase 2: Real S3 data
- Phase 3: Real AI API
- Phase 4: Advanced features

**Benefit:** Working product at each phase

---

## 📊 DATA STRUCTURE

### Current Data Model

```python
# DataFrame structure (works with ANY metrics)
data = pd.DataFrame({
    'date': datetime,              # Date of measurement
    'participantId': str,          # Participant ID (e.g., "BKQ3HJ")
    'participant_type': str,       # "OCD" or "Control"
    
    # Metrics (any column name works)
    'minutesAsleep': int,
    'steps': int,
    'heart_rate': int,
    'vo2max': float,
    # ... add any Fitbit metric
})
```

### Participant Pairing

```python
PARTICIPANT_PAIRS = {
    "PAIR001": {"ocd": "BKQ3HJ", "control": "BRT57L"},
    "PAIR002": {"ocd": "BWPTFS", "control": "BWY5LB"},
    # ... 5 pairs total in sample data
}
```

### Metric Categories

```python
# Sleep metrics (8+)
minutesAsleep, efficiency, timeInBed, deepSleepMinutes, ...

# Activity metrics (10+)
steps, distance, floors, activeMinutes, sedentaryMinutes, ...

# Cardiovascular (8+)
heart_rate, vo2max, heartRateVariability, heartRateZones, ...

# Breathing & Oxygen (4+)
breathingRate, spo2, spo2_avg, ...

# Body metrics (6+)
weight, bmi, bodyFat, muscleMass, ...

# Temperature (3+)
skinTemperature, coreTemperature, ...
```

**Total: 40+ Fitbit metrics supported**

---

## 🔑 CRITICAL IMPLEMENTATION DETAILS

### 1. How AI Insights Work (Current)

**Location:** `utils/ai_assistant.py`

**Functions:**
- `generate_ai_insights(data)` - Single participant analysis
- `generate_comparison_insights(ocd, control, stats)` - OCD vs Control
- `suggest_visualizations(participants, metrics, data)` - Chart suggestions
- `detect_anomalies(data)` - Pattern detection

**Implementation:**
```python
def generate_ai_insights(participant_data):
    # Calculate basic stats
    avg_sleep = participant_data['minutesAsleep'].mean()
    
    # Return hardcoded narrative with stats inserted
    return f"""
    **AI-Generated Analysis Report**
    
    Average sleep: {avg_sleep/60:.1f} hours
    {_interpret_sleep_duration(avg_sleep, participant_type)}
    ...
    """
```

**Future Migration:**
```python
def generate_ai_insights(participant_data):
    client = anthropic.Anthropic(api_key=API_KEY)
    prompt = create_analysis_prompt(participant_data)
    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Cheapest: $0.25/1M tokens
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

### 2. How Data Loading Works (Current)

**Location:** `utils/data_loader.py`

**Key Functions:**
- `get_available_participants()` - List all participants
- `get_participant_pairs()` - List matched pairs
- `load_participant_data(id, date_range)` - Load single participant
- `load_multiple_participants(ids, date_range)` - Load multiple

**Sample Data Generation:**
```python
# Different patterns for OCD vs Control
if participant_type == "OCD":
    base_sleep = 370  # 6.2 hours (reduced)
    base_steps = 7200  # Lower activity
else:
    base_sleep = 450  # 7.5 hours (normal)
    base_steps = 8900  # Higher activity

# Generate realistic data with noise
data['minutesAsleep'] = np.random.normal(base_sleep, std, len(dates))
```

**Future S3 Integration:**
```python
def load_participant_data(participant_id, date_range=None):
    # Load from S3
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(
        Bucket='fitbit-ocd-data',
        Key=f'participants/{participant_id}/sleep_data.csv'
    )
    
    # Parse Fitbit format
    data = pd.read_csv(obj['Body'])
    
    # Standardize column names
    data = standardize_fitbit_columns(data)
    
    return data
```

### 3. How Charts Work

**Location:** `utils/chart_factory.py`

**Pattern:** Generic chart functions

```python
def create_line_chart(data, x, y, color_by=None, title="", **kwargs):
    # Works with ANY x/y column names
    fig = px.line(data, x=x, y=y, color=color_by, title=title, **kwargs)
    return fig
```

**Chart Types:**
- Line Chart (time series)
- Bar Chart (comparisons)
- Scatter Plot (correlations)
- Box Plot (distributions)
- Violin Plot (detailed distributions)
- Area Chart (cumulative)
- Histogram (frequency)

### 4. How Statistics Work

**Location:** `utils/statistical_analysis.py`

**Key Functions:**
- `compare_participants(ocd, control, metrics)` - T-tests, effect sizes
- `calculate_cohens_d(group1, group2)` - Effect size
- `calculate_correlation(data, metric1, metric2)` - Pearson correlation
- `calculate_summary_statistics(data, metric)` - Descriptive stats

**Example:**
```python
def compare_participants(ocd_data, control_data, metrics):
    for metric in metrics:
        # T-test
        t_stat, p_value = stats.ttest_ind(ocd_values, control_values)
        
        # Effect size
        cohens_d = calculate_cohens_d(ocd_values, control_values)
        
        # Interpretation
        significant = p_value < 0.05
        effect_size = interpret_effect_size(cohens_d)
```

---

## 🚀 HOW TO RUN

### Quick Start
```bash
cd streamlit_app
./run.sh
```

### Manual Start
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

**App opens at:** `http://localhost:8501`

---

## 📝 IMPORTANT CONVENTIONS

### Code Style
- **Functions:** snake_case
- **Classes:** PascalCase (minimal use)
- **Constants:** UPPER_CASE in settings.py
- **Files:** snake_case.py
- **Docstrings:** Google style

### Naming Conventions
- **Metrics:** snake_case (e.g., `minutesAsleep`, `heart_rate`)
- **Participants:** UPPERCASE IDs (e.g., `BKQ3HJ`)
- **Pairs:** Format `PAIR001`, `PAIR002`, etc.
- **Session State:** Prefix with page name (e.g., `quick_analysis_data`)

### File Organization
- **Pages:** Numbered with emoji (e.g., `1_🤖_Quick_Analysis.py`)
- **Utils:** Generic, reusable functions
- **Components:** Reusable UI elements
- **Config:** All constants and settings

---

## 🎓 LESSONS LEARNED

### What Worked Well
✅ Streamlit's simplicity accelerated development  
✅ Dummy AI allowed full workflow testing without costs  
✅ Sample data enabled local development  
✅ Three modes serve different user expertise levels  
✅ Metric-agnostic design makes system flexible  
✅ Configuration-driven approach simplifies changes  

### Challenges & Solutions
❌ **Challenge:** Users have varying technical skills  
✅ **Solution:** Three analysis modes (beginner → expert)

❌ **Challenge:** Real data not available during development  
✅ **Solution:** Realistic sample data generator

❌ **Challenge:** AI API costs during development  
✅ **Solution:** Hardcoded responses, easy to swap later

❌ **Challenge:** Many Fitbit metrics to support  
✅ **Solution:** Metric-agnostic architecture

### Design Decisions Rationale

**Decision:** Use Streamlit instead of React + Flask  
**Reason:** Faster development, Python-only, research-friendly  
**Trade-off:** Less UI customization, but acceptable for internal tool

**Decision:** Dummy AI instead of real API  
**Reason:** Zero cost during development, predictable behavior  
**Trade-off:** Not real AI, but easy to migrate later

**Decision:** Sample data instead of real S3  
**Reason:** No AWS dependency, faster iteration  
**Trade-off:** Not real data, but architecture supports both

**Decision:** Three analysis modes  
**Reason:** Serve users with different expertise levels  
**Trade-off:** More code, but better UX

---

## 🔮 FUTURE ROADMAP

### Phase 2: Real Data Integration (Next)
- [ ] AWS S3 connection with boto3
- [ ] Parse Fitbit JSON/CSV exports
- [ ] Data validation pipeline
- [ ] Handle missing/malformed data
- [ ] Automated nightly sync

### Phase 3: Real AI Integration
- [ ] Claude API integration (Anthropic)
- [ ] Dynamic insight generation
- [ ] Cost optimization (caching, batching)
- [ ] Fallback to hardcoded if API fails

### Phase 4: Advanced Features
- [ ] PNG/PDF chart export
- [ ] Comprehensive report generation
- [ ] Saved chart configurations
- [ ] Template library
- [ ] User preferences

### Phase 5: Production Deployment
- [ ] Deploy to Streamlit Cloud or AWS
- [ ] PostgreSQL for processed data
- [ ] Redis caching layer
- [ ] Monitoring & logging
- [ ] User authentication (if needed)

---

## 🐛 KNOWN LIMITATIONS

### Current MVP Limitations
1. **Sample data only** - Not connected to real Fitbit data
2. **Dummy AI** - Hardcoded responses, not real LLM
3. **No export** - PNG/PDF export not implemented yet
4. **No persistence** - Chart configs not saved
5. **Single user** - No authentication/multi-user support
6. **No caching** - Data reloaded on every interaction

### Intentional Limitations (For Now)
- No real-time Fitbit API integration (future)
- No automated report scheduling (future)
- No mobile app (web-only)
- No offline mode (requires internet)

---

## 💡 TIPS FOR FUTURE DEVELOPMENT

### Adding New Metrics
1. Add to `AVAILABLE_METRICS` in `config/settings.py`
2. Add label to `METRIC_LABELS`
3. Add sample data generation in `utils/data_loader.py`
4. Everything else works automatically!

### Adding New Chart Types
1. Add to `CHART_TYPES` in `config/settings.py`
2. Implement function in `utils/chart_factory.py`
3. Add to chart type mapping in custom analysis

### Migrating to Real AI
1. Install: `pip install anthropic`
2. Replace function in `utils/ai_assistant.py`
3. Add API key to environment variables
4. Test with small dataset first (cost control)

### Migrating to Real S3 Data
1. Install: `pip install boto3`
2. Update `load_participant_data()` in `utils/data_loader.py`
3. Add S3 bucket configuration
4. Implement data parsing for Fitbit format
5. Keep sample data as fallback for testing

---

## 📚 IMPORTANT FILES TO UNDERSTAND

### Must Read (Core Logic)
1. **`app.py`** - Main entry point, navigation
2. **`config/settings.py`** - All configuration
3. **`utils/data_loader.py`** - Data loading logic
4. **`utils/ai_assistant.py`** - AI insights (dummy)
5. **`utils/chart_factory.py`** - Chart creation

### Important (Features)
6. **`pages/1_🤖_Quick_Analysis.py`** - Automated analysis
7. **`pages/3_⚙️_Custom_Analysis.py`** - Manual control
8. **`components/participant_selector.py`** - Reusable widget

### Reference (Documentation)
9. **`README.md`** - Technical documentation
10. **`QUICK_START.md`** - User guide
11. **`ADDING_NEW_METRICS.md`** - Metric guide

---

## 🎯 CONTEXT FOR AI ASSISTANTS

### When Starting New Conversation

**Provide this document** and mention:

1. **Current Phase:** MVP with sample data + dummy AI
2. **What Works:** All three modes, visualizations, statistics
3. **What's Dummy:** AI responses, data generation
4. **What's Next:** AWS S3 integration, real AI
5. **Architecture:** Streamlit + Plotly + Pandas
6. **Key Principle:** Metric-agnostic, configuration-driven

### Common Tasks You Might Ask About

**"Add a new metric"**
→ See ADDING_NEW_METRICS.md, update config/settings.py

**"Connect to AWS S3"**
→ Update utils/data_loader.py, use boto3

**"Add real AI"**
→ Update utils/ai_assistant.py, use Claude API

**"Add new chart type"**
→ Update utils/chart_factory.py, add to config

**"Fix a bug"**
→ Check which mode (Quick/Guided/Custom), look at relevant page file

**"Improve UI"**
→ Streamlit uses markdown + components, check app.py or page files

### Project Philosophy

1. **Simplicity over features** - Easy to use > powerful but complex
2. **Progressive complexity** - Start simple, grow as needed
3. **Configuration over code** - Change settings, not logic
4. **Flexibility over optimization** - Works with any metric
5. **Iteration over perfection** - Working product at each phase

---

## ✅ QUICK REFERENCE

### File Locations
- **Config:** `config/settings.py`
- **Data:** `utils/data_loader.py`
- **AI:** `utils/ai_assistant.py`
- **Charts:** `utils/chart_factory.py`
- **Stats:** `utils/statistical_analysis.py`
- **Pages:** `pages/*.py`

### Key Functions
- **Load data:** `load_participant_data(id)`
- **AI insights:** `generate_ai_insights(data)`
- **Create chart:** `create_custom_chart(config)`
- **Statistics:** `compare_participants(ocd, control, metrics)`

### Adding Features
- **New metric:** Edit `config/settings.py` + `utils/data_loader.py`
- **New chart:** Edit `utils/chart_factory.py`
- **New page:** Create `pages/N_emoji_Name.py`
- **New component:** Create `components/name.py`

---

## 📞 PROJECT CONTACTS

**Research Lab:** OCD Research Lab, USC  
**Primary User:** Research Assistants (non-technical)  
**Data Source:** Fitbit wearable devices  
**Deployment:** Local (currently), Streamlit Cloud (future)

---

## 🎉 PROJECT STATUS

### ✅ Completed (MVP)
- [x] Three analysis modes fully functional
- [x] Sample data generation
- [x] Dummy AI with realistic responses
- [x] 7 chart types
- [x] Statistical analysis (t-tests, correlations)
- [x] Participant selection (pairs & individual)
- [x] CSV data export
- [x] Professional UI/UX
- [x] Complete documentation

### 🚧 In Progress
- [ ] None (MVP complete, awaiting next phase)

### 📋 Planned (Future Phases)
- [ ] AWS S3 integration
- [ ] Real AI (Claude API)
- [ ] PNG/PDF export
- [ ] Report generation
- [ ] Production deployment

---

**Last Updated:** 2024-10-09  
**Version:** 1.0 (MVP)  
**Status:** ✅ Ready for use with sample data

---

## 💬 HOW TO USE THIS DOCUMENT

### For New AI Conversations
1. **Share this entire document** at the start
2. **Mention current phase** (MVP with sample data)
3. **State your goal** (e.g., "Add AWS S3 integration")
4. **Reference relevant sections** (e.g., "See Future Roadmap")

### For Team Onboarding
1. Read this document first
2. Then read README.md for technical details
3. Then read QUICK_START.md for usage
4. Run the app and explore all three modes

### For Future Development
1. Check "Future Roadmap" section
2. Review "Known Limitations"
3. Follow patterns in "Key Design Patterns"
4. Maintain "Project Philosophy"

---

**This document should give any AI assistant complete context to continue development seamlessly!** 🚀

