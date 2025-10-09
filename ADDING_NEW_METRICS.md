# 📊 Adding New Fitbit Metrics - Complete Guide

## 🎯 The System is Metric-Agnostic!

The architecture is designed to work with **ANY metric** - not just sleep data. Here's how.

---

## ✅ What Already Works

The system is **already flexible** for any metric because:

1. **Configuration-driven:** Metrics defined in one place
2. **Generic data structure:** Any column name works
3. **Dynamic UI:** Dropdowns populate from config
4. **Universal charts:** Work with any x/y columns
5. **Flexible statistics:** Calculate on any numeric column

---

## 🚀 How to Add ANY New Metric (3 Steps)

### **Step 1: Add to Configuration**

Edit `config/settings.py`:

```python
AVAILABLE_METRICS = [
    # Just add your new metric name here!
    "your_new_metric",
]

METRIC_LABELS = {
    # Add a human-readable label
    "your_new_metric": "Your New Metric (units)",
}
```

### **Step 2: Generate Sample Data**

Edit `utils/data_loader.py` in the `load_participant_data()` function:

```python
data = pd.DataFrame({
    # ... existing columns ...
    
    # Add your new metric with sample data
    'your_new_metric': np.random.normal(mean, std, len(dates)).clip(min, max),
})
```

### **Step 3: Done!**

That's it! The system automatically:
- ✅ Shows it in metric dropdowns
- ✅ Allows charting
- ✅ Calculates statistics
- ✅ Includes in exports
- ✅ Works with AI analysis

---

## 📋 Complete List of Fitbit Metrics

### **Sleep Metrics**
```python
SLEEP_METRICS = [
    # Duration
    "minutesAsleep",
    "minutesAwake", 
    "timeInBed",
    "minutesToFallAsleep",
    "minutesAfterWakeup",
    
    # Quality
    "efficiency",
    "sleepScore",
    "restlessness",
    
    # Sleep Stages
    "deepSleepMinutes",
    "lightSleepMinutes",
    "remSleepMinutes",
    "wakeSleepMinutes",
    
    # Percentages
    "deepSleepPercent",
    "lightSleepPercent",
    "remSleepPercent",
]
```

### **Activity Metrics**
```python
ACTIVITY_METRICS = [
    # Basic Activity
    "steps",
    "distance",
    "floors",
    "elevation",
    
    # Activity Minutes
    "activeMinutes",
    "sedentaryMinutes",
    "lightlyActiveMinutes",
    "fairlyActiveMinutes",
    "veryActiveMinutes",
    
    # Activity Intensity
    "activityLevel",
    "mets",  # Metabolic equivalents
]
```

### **Cardiovascular Metrics**
```python
CARDIOVASCULAR_METRICS = [
    # Heart Rate
    "restingHeartRate",
    "averageHeartRate",
    "maxHeartRate",
    "minHeartRate",
    
    # Heart Rate Zones (minutes in each zone)
    "heartRateZone_outOfRange",
    "heartRateZone_fatBurn",
    "heartRateZone_cardio",
    "heartRateZone_peak",
    
    # Heart Rate Variability
    "heartRateVariability",
    "hrvSDNN",  # Standard deviation
    "hrvRMSSD",  # Root mean square
    
    # Cardiovascular Fitness
    "vo2max",
    "cardioFitnessScore",
]
```

### **Calorie Metrics**
```python
CALORIE_METRICS = [
    "calories",
    "caloriesOut",
    "caloriesBMR",
    "activityCalories",
    "caloriesIn",  # if nutrition data available
]
```

### **Breathing & Oxygen**
```python
BREATHING_METRICS = [
    "breathingRate",
    "spo2",  # Blood oxygen saturation
    "spo2_avg",
    "spo2_min",
    "spo2_max",
]
```

### **Body Metrics**
```python
BODY_METRICS = [
    "weight",
    "bmi",
    "bodyFat",
    "bodyFatPercentage",
    "leanMass",
    "muscleMass",
]
```

### **Temperature**
```python
TEMPERATURE_METRICS = [
    "skinTemperature",
    "skinTemperatureVariation",
    "coreTemperature",
]
```

### **Stress & Recovery**
```python
STRESS_METRICS = [
    "stressScore",
    "recoveryScore",
    "readinessScore",
]
```

---

## 🎨 Real Example: Adding VO2 Max

### Before (Only Sleep + Basic Activity)
```python
# config/settings.py
AVAILABLE_METRICS = [
    "minutesAsleep",
    "steps",
    "heart_rate",
]
```

### After (Added VO2 Max)
```python
# config/settings.py
AVAILABLE_METRICS = [
    "minutesAsleep",
    "steps",
    "heart_rate",
    "vo2max",  # ← NEW!
]

METRIC_LABELS = {
    "minutesAsleep": "Minutes Asleep",
    "steps": "Daily Steps",
    "heart_rate": "Resting Heart Rate (BPM)",
    "vo2max": "VO2 Max (ml/kg/min)",  # ← NEW!
}
```

```python
# utils/data_loader.py
data = pd.DataFrame({
    'date': dates,
    'minutesAsleep': ...,
    'steps': ...,
    'heart_rate': ...,
    'vo2max': np.random.normal(45, 5, len(dates)).clip(30, 70),  # ← NEW!
})
```

**Result:** VO2 Max now appears in all dropdowns and works everywhere!

---

## 🔄 When Loading Real Data from AWS S3

When you switch from sample data to real Fitbit files:

### Option 1: Fitbit API JSON Format
```python
def load_participant_data_from_s3(participant_id):
    # Load JSON from S3
    fitbit_data = load_from_s3(f"{participant_id}/fitbit_data.json")
    
    # Parse Fitbit API format
    data = pd.DataFrame({
        'date': [d['dateTime'] for d in fitbit_data['activities-heart']],
        'heart_rate': [d['value']['restingHeartRate'] for d in fitbit_data['activities-heart']],
        'steps': [d['summary']['steps'] for d in fitbit_data['activities']],
        # ... extract whatever metrics Fitbit provides
    })
    
    return data
```

### Option 2: Fitbit CSV Export
```python
def load_participant_data_from_s3(participant_id):
    # Load CSV from S3
    df = pd.read_csv(f"s3://bucket/{participant_id}/sleep.csv")
    
    # Fitbit CSVs already have column names!
    # Just rename if needed:
    df = df.rename(columns={
        'Minutes Asleep': 'minutesAsleep',
        'Sleep Efficiency': 'efficiency',
        # etc.
    })
    
    return df
```

**The key:** Just make sure the DataFrame has the column names that match your `AVAILABLE_METRICS` list!

---

## 🎯 Metric Categories (Organized)

For better UX, you can organize metrics by category:

```python
# config/settings.py

METRIC_CATEGORIES = {
    "Sleep": [
        "minutesAsleep",
        "efficiency",
        "timeInBed",
        "minutesToFallAsleep",
    ],
    "Activity": [
        "steps",
        "distance",
        "floors",
        "activeMinutes",
    ],
    "Cardiovascular": [
        "heart_rate",
        "vo2max",
        "heartRateVariability",
    ],
    "Breathing": [
        "breathingRate",
        "spo2",
    ],
    "Body": [
        "weight",
        "bmi",
        "bodyFat",
    ],
}

# Then in UI, show categorized dropdowns
```

---

## 💡 Pro Tips

### **1. Metric Units Matter**
Always include units in labels:
```python
METRIC_LABELS = {
    "distance": "Distance (miles)",  # ✅ Good
    "distance": "Distance",           # ❌ Ambiguous
}
```

### **2. Use Appropriate Data Types**
```python
# Integer metrics
"steps": int
"floors": int

# Float metrics  
"distance": float (1 decimal)
"efficiency": float (1 decimal)
"vo2max": float (1 decimal)

# Percentage metrics
"efficiency": 0-100 scale
"spo2": 0-100 scale
```

### **3. Handle Missing Data**
```python
# Some metrics may not be available for all dates
data['vo2max'] = data['vo2max'].fillna(method='ffill')  # Forward fill
# OR
data['vo2max'] = data['vo2max'].fillna(data['vo2max'].mean())  # Mean imputation
```

### **4. Metric-Specific Validation**
```python
# Add validation for realistic ranges
data['spo2'] = data['spo2'].clip(85, 100)  # Blood oxygen
data['heart_rate'] = data['heart_rate'].clip(40, 120)  # Resting HR
data['steps'] = data['steps'].clip(0, 50000)  # Daily steps
```

---

## 🧪 Testing New Metrics

After adding a new metric:

1. **Run the app:**
   ```bash
   streamlit run app.py
   ```

2. **Check Custom Analysis:**
   - Go to Custom Analysis
   - Select your new metric from dropdown
   - Verify it appears in both X and Y axis options

3. **Create a chart:**
   - Build a line chart with your new metric
   - Verify data displays correctly

4. **Check statistics:**
   - Go to "Additional Analysis" → "Summary Statistics"
   - Verify calculations are correct

5. **Test AI analysis:**
   - Run Quick Analysis
   - Check if new metric is included in insights

---

## 📊 Example: Complete Fitbit Metrics Setup

Here's a comprehensive example with ALL major Fitbit metrics:

```python
# config/settings.py

AVAILABLE_METRICS = [
    # Sleep (8 metrics)
    "minutesAsleep",
    "minutesAwake",
    "efficiency",
    "timeInBed",
    "minutesToFallAsleep",
    "deepSleepMinutes",
    "lightSleepMinutes",
    "remSleepMinutes",
    
    # Activity (6 metrics)
    "steps",
    "distance",
    "floors",
    "activeMinutes",
    "sedentaryMinutes",
    "veryActiveMinutes",
    
    # Cardiovascular (5 metrics)
    "heart_rate",
    "vo2max",
    "heartRateVariability",
    "heartRateZone_fatBurn",
    "heartRateZone_cardio",
    
    # Calories (3 metrics)
    "calories",
    "caloriesBMR",
    "activityCalories",
    
    # Breathing & Oxygen (2 metrics)
    "breathingRate",
    "spo2",
    
    # Body (3 metrics)
    "weight",
    "bmi",
    "bodyFat",
]

# Total: 27 metrics covering all major Fitbit data types!
```

---

## ✅ Summary

### **The System is Already Flexible!**

- ✅ Works with ANY metric name
- ✅ No hardcoded sleep-specific logic
- ✅ Add metrics in 3 simple steps
- ✅ Charts, stats, AI all work automatically
- ✅ Easy to extend for real Fitbit data

### **Current Implementation:**
- **Focused on sleep** for demo purposes
- **Architecture supports ALL metrics**
- **Easy to add more** as needed

### **When You Get Real Data:**
- Parse Fitbit JSON/CSV
- Map to your metric names
- Everything else works automatically!

---

**The system is ready for ANY Fitbit metric you throw at it!** 🚀
