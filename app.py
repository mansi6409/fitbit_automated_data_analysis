"""
OCD Fitbit Data Analysis Platform
Main Streamlit Application
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config.settings import APP_TITLE, APP_ICON

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ AUTHENTICATION ============
from utils.auth import check_authentication, show_user_info, logout_button

if not check_authentication():
    st.stop()

# Show user info and logout in sidebar
show_user_info()
logout_button()
# ========================================

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f9fafb;
        border-radius: 0.5rem;
        padding: 1rem;
        border-left: 4px solid #3b82f6;
    }
    .info-box {
        background-color: #eff6ff;
        border-radius: 0.5rem;
        padding: 1rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fdf4;
        border-radius: 0.5rem;
        padding: 1rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown(f"# {APP_ICON} {APP_TITLE}")
    st.markdown("---")
    
    st.markdown("### 🎯 Select Your Workflow")
    
    # Mode description
    with st.expander("ℹ️ What's the difference?"):
        st.markdown("""
        **🤖 Quick AI Analysis**
        - One-click automated analysis
        - AI generates insights automatically
        - Best for: Quick overview, beginners
        
        **🎯 Guided Analysis**
        - AI suggests, you choose
        - Balance of automation + control
        - Best for: Most users, most tasks
        
        **⚙️ Custom Analysis**
        - Full manual control
        - Customize everything
        - Best for: Expert users, specific needs
        """)
    
    # Session state for current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

# Main content
st.markdown('<div class="main-header">🔬 OCD Fitbit Data Analysis Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Compare OCD participants with healthy controls using interactive visualizations and AI-powered insights</div>', unsafe_allow_html=True)

# Welcome section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>🤖 Quick AI Analysis</h3>
        <p>Let AI do the work for you. One-click automated analysis with instant insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Quick Analysis", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🤖_Quick_Analysis.py")

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 Guided Analysis</h3>
        <p>AI-assisted workflow. Get suggestions while maintaining full control.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Guided Analysis", use_container_width=True):
        st.switch_page("pages/2_🎯_Guided_Analysis.py")

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>⚙️ Custom Analysis</h3>
        <p>Full manual control. Build custom visualizations from scratch.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Custom Analysis", use_container_width=True):
        st.switch_page("pages/3_⚙️_Custom_Analysis.py")

st.markdown("---")

# Quick stats section
st.subheader("📊 Platform Overview")

from utils.data_loader import get_available_participants, get_participant_pairs

participants = get_available_participants()
pairs = get_participant_pairs()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Participants",
        len(participants),
        help="Total number of participants in the study"
    )

with col2:
    ocd_count = sum(1 for p in participants if p['type'] == 'OCD')
    st.metric(
        "🔴 OCD Participants",
        ocd_count,
        help="Participants diagnosed with OCD"
    )

with col3:
    control_count = sum(1 for p in participants if p['type'] == 'Control')
    st.metric(
        "🟢 Control Participants",
        control_count,
        help="Healthy control participants"
    )

with col4:
    st.metric(
        "Matched Pairs",
        len(pairs),
        help="OCD-Control matched pairs"
    )

st.markdown("---")

# Feature highlights
st.subheader("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📈 Comprehensive Analytics**
    - Sleep duration and quality metrics
    - Activity levels and patterns
    - Heart rate monitoring
    - Statistical comparisons
    
    **🤖 AI-Powered Insights**
    - Automated pattern detection
    - Anomaly identification
    - Natural language summaries
    - Chart recommendations
    """)

with col2:
    st.markdown("""
    **🎨 Flexible Visualizations**
    - Line charts, bar charts, scatter plots
    - Box plots, violin plots, heatmaps
    - Customizable colors and styles
    - Export as PNG, PDF, or CSV
    
    **👥 Easy Participant Management**
    - View by pairs or individuals
    - Quick pair selection
    - Side-by-side comparisons
    - Data quality indicators
    """)

st.markdown("---")

# Getting started guide
with st.expander("📚 Getting Started Guide"):
    st.markdown("""
    ### How to Use This Platform
    
    #### Step 1: Choose Your Workflow
    - **New users?** Start with **Quick AI Analysis** for automated insights
    - **Experienced?** Use **Guided Analysis** for more control
    - **Expert?** Try **Custom Analysis** for full flexibility
    
    #### Step 2: Select Participants
    - Choose individual participants or matched pairs
    - OCD participants are marked with 🔴
    - Control participants are marked with 🟢
    
    #### Step 3: Analyze Data
    - View AI-generated insights
    - Explore interactive visualizations
    - Run statistical tests
    - Export results
    
    #### Step 4: Export & Share
    - Download charts as images (PNG, PDF)
    - Export data as CSV
    - Generate comprehensive reports
    
    ### Tips for Best Results
    - ✅ Always compare OCD with matched controls
    - ✅ Check date ranges to ensure comparable periods
    - ✅ Look for data quality warnings
    - ✅ Use multiple chart types for comprehensive analysis
    - ✅ Pay attention to AI suggestions and anomaly warnings
    """)

# Footer
st.markdown("---")
st.caption("🔬 OCD Fitbit Data Analysis Platform | Built with Streamlit + Plotly + AI")

