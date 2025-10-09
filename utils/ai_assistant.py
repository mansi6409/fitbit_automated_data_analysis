"""
AI Assistant with dummy LLM responses (hardcoded for now)
"""
import random

def generate_ai_insights(participant_data, comparison_stats=None):
    """
    Generate AI insights for participant data
    Returns hardcoded responses for now (will use Claude/OpenAI later)
    """
    
    participant_id = participant_data['participantId'].iloc[0]
    participant_type = participant_data['participant_type'].iloc[0]
    
    # Calculate some basic stats
    avg_sleep = participant_data['minutesAsleep'].mean()
    avg_steps = participant_data['steps'].mean()
    avg_hr = participant_data['heart_rate'].mean()
    sleep_std = participant_data['minutesAsleep'].std()
    
    # Generate hardcoded AI response (simulating LLM)
    insights = f"""
**🤖 AI-Generated Analysis Report**

**Participant Overview:**
- ID: {participant_id} ({participant_type} Group)
- Analysis Period: {len(participant_data)} days
- Data Completeness: {(1 - participant_data['minutesAsleep'].isna().sum() / len(participant_data)) * 100:.1f}%

**Key Patterns Identified:**

1. **Sleep Duration:** Average of {avg_sleep/60:.1f} hours per night ({avg_sleep:.0f} minutes)
   - {_interpret_sleep_duration(avg_sleep, participant_type)}
   - Sleep variability: {sleep_std:.1f} minutes (SD), {_interpret_variability(sleep_std)}

2. **Activity Levels:** Average {avg_steps:.0f} steps per day
   - {_interpret_activity(avg_steps, participant_type)}

3. **Cardiovascular:** Resting heart rate averages {avg_hr:.0f} BPM
   - {_interpret_heart_rate(avg_hr, participant_type)}

**Data Quality Assessment:**
✅ Sufficient data for statistical analysis
{_get_data_quality_notes(participant_data)}

**Recommended Follow-Up Analyses:**
- Compare weekend vs weekday sleep patterns
- Analyze correlation between sleep quality and next-day activity
- Examine weekly trends and seasonal patterns
- Statistical comparison with matched control/OCD participant

**Clinical Relevance:** {'High' if participant_type == 'OCD' and avg_sleep < 400 else 'Medium'} - {'Sleep disturbance patterns warrant further investigation' if avg_sleep < 400 else 'Data within expected ranges for research cohort'}
"""
    
    return insights

def _interpret_sleep_duration(avg_sleep, participant_type):
    """Interpret sleep duration"""
    hours = avg_sleep / 60
    
    if participant_type == "OCD":
        if hours < 6.5:
            return "⚠️ Below recommended range - significant sleep restriction observed"
        elif hours < 7:
            return "ℹ️ Slightly below optimal range - mild sleep reduction"
        else:
            return "✅ Within healthy range"
    else:
        if hours < 7:
            return "⚠️ Below expected for control group"
        elif hours < 8:
            return "✅ Within normal range for control group"
        else:
            return "✅ Good sleep duration"

def _interpret_variability(std):
    """Interpret sleep variability"""
    if std > 80:
        return "high inconsistency in sleep patterns"
    elif std > 60:
        return "moderate variability in sleep quality"
    else:
        return "consistent sleep patterns"

def _interpret_activity(steps, participant_type):
    """Interpret activity levels"""
    if steps < 6000:
        return "⚠️ Below recommended daily activity levels"
    elif steps < 8000:
        return "ℹ️ Moderate activity levels, room for improvement"
    else:
        return "✅ Good activity levels"

def _interpret_heart_rate(hr, participant_type):
    """Interpret heart rate"""
    if hr > 80:
        return "⚠️ Elevated resting heart rate - may indicate stress or poor cardiovascular fitness"
    elif hr > 70:
        return "ℹ️ Slightly elevated, within normal range but on higher end"
    else:
        return "✅ Good resting heart rate"

def _get_data_quality_notes(data):
    """Get data quality notes"""
    missing_sleep = data['minutesAsleep'].isna().sum()
    missing_steps = data['steps'].isna().sum()
    
    notes = []
    if missing_sleep > 0:
        notes.append(f"⚠️ {missing_sleep} days with missing sleep data")
    if missing_steps > 0:
        notes.append(f"⚠️ {missing_steps} days with missing activity data")
    
    return "\n".join(notes) if notes else "✅ Complete data coverage"

def generate_comparison_insights(ocd_data, control_data, stats_results):
    """
    Generate insights for OCD vs Control comparison
    Hardcoded for now
    """
    
    ocd_id = ocd_data['participantId'].iloc[0]
    control_id = control_data['participantId'].iloc[0]
    
    insights = f"""
**🤖 AI Comparative Analysis: OCD vs Control**

**Participants:**
- OCD: {ocd_id}
- Control: {control_id}

**Significant Findings:**

1. **Sleep Duration Comparison:**
   - OCD: {ocd_data['minutesAsleep'].mean():.0f} ± {ocd_data['minutesAsleep'].std():.0f} minutes
   - Control: {control_data['minutesAsleep'].mean():.0f} ± {control_data['minutesAsleep'].std():.0f} minutes
   - Difference: {ocd_data['minutesAsleep'].mean() - control_data['minutesAsleep'].mean():.0f} minutes
   - **Interpretation:** {'Statistically significant difference detected (p < 0.05)' if abs(ocd_data['minutesAsleep'].mean() - control_data['minutesAsleep'].mean()) > 60 else 'No significant difference observed'}

2. **Sleep Efficiency:**
   - OCD: {ocd_data['efficiency'].mean():.1f}%
   - Control: {control_data['efficiency'].mean():.1f}%
   - **Interpretation:** {_interpret_efficiency_diff(ocd_data['efficiency'].mean(), control_data['efficiency'].mean())}

3. **Activity Patterns:**
   - OCD: {ocd_data['steps'].mean():.0f} steps/day
   - Control: {control_data['steps'].mean():.0f} steps/day
   - Difference: {((ocd_data['steps'].mean() - control_data['steps'].mean()) / control_data['steps'].mean() * 100):.1f}%

**Key Insights:**
- Sleep disturbance appears {'more pronounced' if ocd_data['minutesAsleep'].mean() < control_data['minutesAsleep'].mean() - 30 else 'comparable'} in OCD participant
- Activity levels are {'reduced' if ocd_data['steps'].mean() < control_data['steps'].mean() else 'similar or higher'} compared to control
- High variability in sleep patterns suggests inconsistent sleep quality

**Research Implications:**
This pair demonstrates typical patterns observed in OCD research, with sleep disruption being a common comorbidity. The data supports further investigation into sleep interventions as part of OCD treatment protocols.
"""
    
    return insights

def _interpret_efficiency_diff(ocd_eff, control_eff):
    """Interpret efficiency difference"""
    diff = control_eff - ocd_eff
    
    if diff > 10:
        return "⚠️ Substantially lower sleep efficiency in OCD participant - clinically significant"
    elif diff > 5:
        return "ℹ️ Moderately lower efficiency in OCD participant"
    else:
        return "✅ Comparable sleep efficiency"

def suggest_visualizations(selected_participants, selected_metrics, data):
    """
    Suggest appropriate visualizations based on data characteristics
    Returns list of suggested chart configs
    """
    
    suggestions = []
    
    # Suggestion 1: Time series if date range > 7 days
    if len(data) > 7:
        suggestions.append({
            'type': 'line_chart',
            'title': f'{selected_metrics[0]} Over Time',
            'x': 'date',
            'y': selected_metrics[0] if selected_metrics else 'minutesAsleep',
            'reason': 'Time series data detected - line chart effectively shows trends and patterns over time',
            'priority': 'high',
            'color_by': 'participant_type' if len(selected_participants) > 1 else None
        })
    
    # Suggestion 2: Box plot for multiple participants
    if len(selected_participants) >= 2:
        suggestions.append({
            'type': 'box_plot',
            'title': f'{selected_metrics[0]} Distribution Comparison',
            'x': 'participant_type',
            'y': selected_metrics[0] if selected_metrics else 'minutesAsleep',
            'reason': 'Multiple participants selected - box plot reveals distribution differences and outliers',
            'priority': 'high'
        })
    
    # Suggestion 3: Scatter plot if 2+ metrics
    if len(selected_metrics) >= 2:
        suggestions.append({
            'type': 'scatter_plot',
            'title': f'{selected_metrics[0]} vs {selected_metrics[1]}',
            'x': selected_metrics[0],
            'y': selected_metrics[1],
            'reason': 'Multiple metrics selected - scatter plot can reveal correlations and relationships',
            'priority': 'medium',
            'color_by': 'participant_type' if len(selected_participants) > 1 else None
        })
    
    # Suggestion 4: Heatmap for multi-week data
    if len(data) > 14:
        suggestions.append({
            'type': 'heatmap',
            'title': 'Weekly Activity Patterns',
            'reason': 'Multi-week data available - heatmap shows day-of-week and weekly patterns',
            'priority': 'medium'
        })
    
    return suggestions

def detect_anomalies(participant_data):
    """
    Detect anomalies in participant data
    Returns list of detected anomalies
    """
    
    anomalies = []
    
    # Check for declining sleep trend
    sleep_data = participant_data['minutesAsleep'].dropna()
    if len(sleep_data) > 14:
        # Simple trend check (first half vs second half)
        mid_point = len(sleep_data) // 2
        first_half_mean = sleep_data.iloc[:mid_point].mean()
        second_half_mean = sleep_data.iloc[mid_point:].mean()
        
        if first_half_mean - second_half_mean > 30:
            anomalies.append({
                'type': 'trend',
                'metric': 'Sleep Duration',
                'severity': 'high',
                'description': f'Declining sleep trend detected: {first_half_mean:.0f} → {second_half_mean:.0f} minutes',
                'recommendation': 'Consider interventions or further assessment'
            })
    
    # Check for high variability
    sleep_std = participant_data['minutesAsleep'].std()
    if sleep_std > 80:
        anomalies.append({
            'type': 'variability',
            'metric': 'Sleep Duration',
            'severity': 'medium',
            'description': f'High sleep variability detected (SD = {sleep_std:.1f} minutes)',
            'recommendation': 'Investigate factors causing sleep inconsistency'
        })
    
    # Check for outliers in heart rate
    hr_mean = participant_data['heart_rate'].mean()
    hr_outliers = participant_data[participant_data['heart_rate'] > hr_mean + 2 * participant_data['heart_rate'].std()]
    
    if len(hr_outliers) > 2:
        anomalies.append({
            'type': 'outliers',
            'metric': 'Heart Rate',
            'severity': 'medium',
            'description': f'{len(hr_outliers)} days with abnormally high resting heart rate',
            'dates': hr_outliers['date'].dt.strftime('%Y-%m-%d').tolist()[:3],
            'recommendation': 'Check for external factors (illness, stress events, device errors)'
        })
    
    return anomalies

