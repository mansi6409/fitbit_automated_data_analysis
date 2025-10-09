# 🤖 Instructions for AI Assistants

**If you're an AI assistant helping with this project, read this first!**

---

## 📋 Quick Orientation

### What You're Working On
A Streamlit-based data analysis platform for OCD research. Users are research assistants (non-technical) comparing OCD participants vs healthy controls using Fitbit data.

### Current State
- ✅ **Working:** Full MVP with sample data and dummy AI
- 🚧 **Next:** AWS S3 integration and real AI (Claude API)
- 📍 **Location:** `/Users/mansigarg/USC/LAB/ocd-research-app/dataanalysis/streamlit_app/`

### Key Files to Know
```
config/settings.py          # All configuration (metrics, pairs, etc.)
utils/data_loader.py        # Data loading (currently sample data)
utils/ai_assistant.py       # AI insights (currently hardcoded)
utils/chart_factory.py      # Plotly chart creation
pages/*.py                  # Three analysis modes
```

---

## 🎯 Important Context

### Architecture Decisions

**Streamlit (not React)** - Faster development, Python-only  
**Dummy AI (not real API)** - Zero cost during development  
**Sample Data (not S3)** - No AWS dependency yet  
**Three Modes** - Beginner → Intermediate → Expert  

### Design Principles

1. **Metric-Agnostic** - System works with ANY Fitbit metric, not just sleep
2. **Configuration-Driven** - Add metrics in config, not code
3. **Progressive Complexity** - Easy mode → Advanced mode
4. **Component Reusability** - DRY principle throughout

### What's "Dummy" vs "Real"

**Dummy (Current):**
- AI responses are hardcoded in `utils/ai_assistant.py`
- Data is generated programmatically in `utils/data_loader.py`

**Real (Future):**
- AI will use Claude API (Anthropic)
- Data will load from AWS S3 bucket

**Important:** The architecture supports both! Easy to migrate.

---

## 🚨 Critical Things to Remember

### 1. The System is NOT Sleep-Specific
Even though sample data focuses on sleep, the architecture is **metric-agnostic**. It works with ANY Fitbit metric:
- Sleep (duration, efficiency, stages)
- Activity (steps, distance, floors)
- Cardiovascular (heart rate, VO2 max, HRV)
- Breathing (breathing rate, SpO2)
- Body (weight, BMI, body fat)
- And 40+ more metrics

### 2. Adding Metrics is Easy (3 Steps)
```python
# Step 1: config/settings.py
AVAILABLE_METRICS.append("new_metric")
METRIC_LABELS["new_metric"] = "New Metric (units)"

# Step 2: utils/data_loader.py
data['new_metric'] = np.random.normal(mean, std, len(dates))

# Step 3: Done! Everything else works automatically
```

### 3. Don't Break the Dummy Implementations
The hardcoded AI and sample data are **intentional**. Don't try to "fix" them by adding real APIs unless explicitly asked. They're designed to work without external dependencies.

### 4. Three Modes Serve Different Users
- **Quick AI:** For beginners, fully automated
- **Guided:** For most users, AI-assisted
- **Custom:** For experts, full control

Don't consolidate them - they serve different purposes!

### 5. Configuration Over Code
When adding features, prefer updating `config/settings.py` over changing logic. The system is designed to be configuration-driven.

---

## 📝 Common Requests & How to Handle

### "Add a new metric"
→ Update `config/settings.py` and `utils/data_loader.py`  
→ See ADDING_NEW_METRICS.md for details  
→ Don't change chart/stats logic (they're already generic)

### "Connect to AWS S3"
→ Update `utils/data_loader.py`  
→ Use boto3 to fetch from S3  
→ Keep sample data as fallback for testing  
→ See PROJECT_CONTEXT.md "Future Roadmap"

### "Add real AI"
→ Update `utils/ai_assistant.py`  
→ Use Claude API (Anthropic) - cheapest option  
→ Keep hardcoded responses as fallback  
→ Add API key to environment variables

### "Add new chart type"
→ Update `utils/chart_factory.py`  
→ Add to `CHART_TYPES` in `config/settings.py`  
→ Update chart type mapping in custom analysis page

### "Fix a bug"
→ Ask which mode (Quick/Guided/Custom)  
→ Check relevant page file in `pages/`  
→ Check if issue is in shared utils  
→ Test in all three modes if changing utils

### "Improve UI"
→ Streamlit uses markdown + components  
→ Check `app.py` for home page  
→ Check `pages/*.py` for mode-specific UI  
→ Use Streamlit's built-in widgets when possible

### "Optimize performance"
→ Current focus is functionality, not optimization  
→ Performance optimization is Phase 5 (future)  
→ Unless it's unusably slow, defer optimization

---

## 🎓 Code Patterns to Follow

### 1. Generic Functions
```python
# ✅ Good - works with any metric
def create_chart(data, x, y):
    fig = px.line(data, x=x, y=y)

# ❌ Bad - hardcoded for sleep
def create_sleep_chart(data):
    fig = px.line(data, x='date', y='minutesAsleep')
```

### 2. Configuration-Driven
```python
# ✅ Good - uses config
from config.settings import AVAILABLE_METRICS
metrics = AVAILABLE_METRICS

# ❌ Bad - hardcoded list
metrics = ["minutesAsleep", "steps", "heart_rate"]
```

### 3. Reusable Components
```python
# ✅ Good - reusable component
from components.participant_selector import participant_selector
selected = participant_selector(mode="mixed")

# ❌ Bad - duplicate code in each page
selected = st.multiselect("Select participants", ...)
```

### 4. Dummy Implementation Pattern
```python
# ✅ Good - easy to migrate
def generate_insights(data):
    # TODO: Replace with Claude API
    return "Hardcoded insight based on data..."

# ❌ Bad - requires API during development
def generate_insights(data):
    client = anthropic.Anthropic(api_key=KEY)
    return client.messages.create(...)
```

---

## 🔍 Where to Find Things

### Configuration
**File:** `config/settings.py`  
**Contains:** Metrics, pairs, chart types, color palettes, all constants

### Data Loading
**File:** `utils/data_loader.py`  
**Functions:** `load_participant_data()`, `get_available_participants()`, etc.  
**Current:** Sample data generation  
**Future:** AWS S3 loading

### AI Insights
**File:** `utils/ai_assistant.py`  
**Functions:** `generate_ai_insights()`, `suggest_visualizations()`, etc.  
**Current:** Hardcoded responses  
**Future:** Claude API

### Charts
**File:** `utils/chart_factory.py`  
**Functions:** `create_line_chart()`, `create_bar_chart()`, etc.  
**Pattern:** Generic, works with any x/y columns

### Statistics
**File:** `utils/statistical_analysis.py`  
**Functions:** `compare_participants()`, `calculate_correlation()`, etc.  
**Uses:** SciPy for t-tests, correlations, effect sizes

### UI Pages
**Files:** `pages/1_🤖_Quick_Analysis.py`, `pages/2_🎯_Guided_Analysis.py`, etc.  
**Pattern:** Each mode is a separate page

---

## ⚠️ Things NOT to Do

### ❌ Don't Add Real APIs Without Being Asked
The dummy implementations are intentional. Don't "fix" them.

### ❌ Don't Hardcode Metric Names in Logic
Use configuration and generic functions instead.

### ❌ Don't Consolidate the Three Modes
They serve different user needs. Keep them separate.

### ❌ Don't Remove Sample Data
Keep it as a fallback even after adding S3.

### ❌ Don't Optimize Prematurely
Focus on functionality first, optimization later.

### ❌ Don't Add Complex Dependencies
Keep the stack simple: Streamlit, Plotly, Pandas, SciPy.

### ❌ Don't Change the Architecture Without Discussion
The current design is intentional and well-thought-out.

---

## ✅ Things TO Do

### ✅ Follow Existing Patterns
Look at how things are done and maintain consistency.

### ✅ Update Configuration First
Add to config before changing code.

### ✅ Test in All Three Modes
If changing shared utils, test Quick, Guided, and Custom modes.

### ✅ Keep It Simple
Prefer simple solutions over clever ones.

### ✅ Document Decisions
Update PROJECT_CONTEXT.md if making architectural changes.

### ✅ Maintain Metric-Agnostic Design
Ensure new features work with any metric, not just sleep.

### ✅ Ask for Clarification
If requirements are unclear, ask before implementing.

---

## 📚 Documentation Hierarchy

1. **AI_INSTRUCTIONS.md** (this file) - Start here
2. **QUICK_CONTEXT.md** - Quick reference
3. **PROJECT_CONTEXT.md** - Complete context
4. **README.md** - Technical documentation
5. **QUICK_START.md** - User guide
6. **ADDING_NEW_METRICS.md** - Metric guide

**Read in order:** AI_INSTRUCTIONS → QUICK_CONTEXT → PROJECT_CONTEXT

---

## 🎯 Your Goal

Help the user extend and improve this platform while:
1. **Maintaining simplicity** - Easy for non-technical users
2. **Following patterns** - Consistent with existing code
3. **Staying flexible** - Works with any Fitbit metric
4. **Being pragmatic** - Working product over perfect code

---

## 💬 How to Start a Conversation

**User will likely say:** "I want to add [feature]" or "Can you help with [task]"

**You should:**
1. Confirm you've read this document
2. Ask clarifying questions if needed
3. Suggest approach following existing patterns
4. Implement maintaining the architecture
5. Test thoroughly
6. Update documentation if needed

---

## 🚀 Quick Commands

### Run the App
```bash
cd /Users/mansigarg/USC/LAB/ocd-research-app/dataanalysis/streamlit_app
streamlit run app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Key Directories
- **Config:** `config/`
- **Utils:** `utils/`
- **Pages:** `pages/`
- **Components:** `components/`

---

## 🎓 Philosophy

This project values:
1. **Simplicity** over features
2. **Usability** over power
3. **Flexibility** over optimization
4. **Iteration** over perfection
5. **Configuration** over code

Keep this in mind when making suggestions!

---

**You're ready to help! Good luck! 🚀**

