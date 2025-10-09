"""
Application configuration and settings
"""

# Data paths
SAMPLE_DATA_DIR = "../sample-data"
SLEEP_DATA_DIR = "../sleep-data"
COMBINED_DATA_FILE = "../sleep-data/sleep_meta_combined.csv"

# Participant metadata
PARTICIPANT_PAIRS = {
    "PAIR001": {"ocd": "BKQ3HJ", "control": "BRT57L"},
    "PAIR002": {"ocd": "BWPTFS", "control": "BWY5LB"},
    "PAIR003": {"ocd": "BX8KLH", "control": "BX8NTV"},
    "PAIR004": {"ocd": "BXMMHR", "control": "BYG334"},
    "PAIR005": {"ocd": "BZCKBJ", "control": "C227P4"},
}

# Available metrics
AVAILABLE_METRICS = [
    # Sleep metrics
    "minutesAsleep",
    "minutesAwake",
    "efficiency",
    "timeInBed",
    "minutesToFallAsleep",
    "minutesAfterWakeup",
    
    # Activity metrics
    "steps",
    "distance",
    "floors",
    "activeMinutes",
    
    # Cardiovascular metrics
    "heart_rate",
    "vo2max",
    
    # Calories
    "calories",
    
    # Breathing & Oxygen
    "breathingRate",
    "spo2",
]

# Metric display names
METRIC_LABELS = {
    # Sleep
    "minutesAsleep": "Minutes Asleep",
    "minutesAwake": "Minutes Awake",
    "efficiency": "Sleep Efficiency (%)",
    "timeInBed": "Time in Bed (minutes)",
    "minutesToFallAsleep": "Minutes to Fall Asleep",
    "minutesAfterWakeup": "Minutes After Wakeup",
    
    # Activity
    "steps": "Daily Steps",
    "distance": "Distance (miles)",
    "floors": "Floors Climbed",
    "activeMinutes": "Active Minutes",
    
    # Cardiovascular
    "heart_rate": "Resting Heart Rate (BPM)",
    "vo2max": "VO2 Max (ml/kg/min)",
    
    # Calories
    "calories": "Calories Burned",
    
    # Breathing & Oxygen
    "breathingRate": "Breathing Rate (breaths/min)",
    "spo2": "Blood Oxygen Saturation (%)",
}

# Chart types
CHART_TYPES = [
    "Line Chart",
    "Bar Chart",
    "Scatter Plot",
    "Box Plot",
    "Violin Plot",
    "Area Chart",
    "Histogram",
    "Heatmap",
]

# Color palettes
COLOR_PALETTES = {
    "Default": ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"],
    "Colorblind-safe": ["#0173B2", "#DE8F05", "#029E73", "#CC78BC", "#CA9161"],
    "Viridis": ["#440154", "#31688e", "#35b779", "#fde724"],
    "Plasma": ["#0d0887", "#7e03a8", "#cc4778", "#f89540", "#f0f921"],
}

# Statistical significance threshold
ALPHA = 0.05

# App theme
APP_TITLE = "OCD Fitbit Data Analysis Platform"
APP_ICON = "🔬"

