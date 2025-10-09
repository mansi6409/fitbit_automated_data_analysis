"""
Data loading utilities for sample Fitbit data
"""
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np

def get_available_participants():
    """Get list of all available participants"""
    from config.settings import PARTICIPANT_PAIRS
    
    participants = []
    for pair_id, pair_info in PARTICIPANT_PAIRS.items():
        participants.append({
            "id": pair_info["ocd"],
            "type": "OCD",
            "pair_id": pair_id
        })
        participants.append({
            "id": pair_info["control"],
            "type": "Control",
            "pair_id": pair_id
        })
    
    return participants

def get_participant_pairs():
    """Get list of participant pairs"""
    from config.settings import PARTICIPANT_PAIRS
    
    pairs = []
    for pair_id, pair_info in PARTICIPANT_PAIRS.items():
        pairs.append({
            "pair_id": pair_id,
            "ocd_id": pair_info["ocd"],
            "control_id": pair_info["control"],
            "ocd_record_count": 90,  # Dummy count
            "control_record_count": 90,
            "ocd_date_range": "2023-06-01 to 2023-08-31",
            "control_date_range": "2023-06-01 to 2023-08-31"
        })
    
    return pairs

def load_participant_data(participant_id, date_range=None):
    """
    Load data for a specific participant
    For now, generates sample data
    """
    # Generate sample data for demonstration
    start_date = datetime(2023, 6, 1)
    end_date = datetime(2023, 8, 31)
    
    if date_range:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate realistic sample data based on participant type
    participant_type = get_participant_type(participant_id)
    
    # Different patterns for OCD vs Control
    if participant_type == "OCD":
        base_sleep = 370  # 6.2 hours in minutes
        sleep_std = 65
        base_steps = 7200
        steps_std = 2100
        base_hr = 75
    else:
        base_sleep = 450  # 7.5 hours in minutes
        sleep_std = 50
        base_steps = 8900
        steps_std = 1800
        base_hr = 68
    
    # Generate data with some realistic patterns
    data = pd.DataFrame({
        'date': dates,
        'participantId': participant_id,
        'participant_type': participant_type,
        
        # Sleep metrics
        'minutesAsleep': np.random.normal(base_sleep, sleep_std, len(dates)).clip(180, 600),
        'minutesAwake': np.random.normal(60, 20, len(dates)).clip(10, 150),
        'efficiency': np.random.normal(85 if participant_type == "Control" else 73, 8, len(dates)).clip(50, 100),
        'timeInBed': np.random.normal(base_sleep + 60, 70, len(dates)).clip(200, 650),
        'minutesToFallAsleep': np.random.normal(15, 8, len(dates)).clip(0, 60),
        'minutesAfterWakeup': np.random.normal(10, 5, len(dates)).clip(0, 30),
        
        # Activity metrics
        'steps': np.random.normal(base_steps, steps_std, len(dates)).clip(1000, 20000),
        'distance': np.random.normal(base_steps / 2000, steps_std / 2000, len(dates)).clip(0.5, 15),  # miles (rough conversion)
        'floors': np.random.normal(12 if participant_type == "Control" else 8, 4, len(dates)).clip(0, 40),
        'activeMinutes': np.random.normal(45 if participant_type == "Control" else 35, 15, len(dates)).clip(0, 180),
        
        # Cardiovascular metrics
        'heart_rate': np.random.normal(base_hr, 6, len(dates)).clip(55, 95),
        'vo2max': np.random.normal(48 if participant_type == "Control" else 42, 5, len(dates)).clip(30, 70),
        
        # Calories
        'calories': np.random.normal(2200, 300, len(dates)).clip(1500, 3500),
        
        # Breathing & Oxygen
        'breathingRate': np.random.normal(16, 2, len(dates)).clip(12, 24),
        'spo2': np.random.normal(97, 1.5, len(dates)).clip(92, 100),
    })
    
    # Round values appropriately
    # Integer metrics
    for col in ['minutesAsleep', 'minutesAwake', 'timeInBed', 'minutesToFallAsleep', 
                'minutesAfterWakeup', 'steps', 'calories', 'floors', 'activeMinutes', 
                'heart_rate', 'breathingRate']:
        if col in data.columns:
            data[col] = data[col].round(0).astype(int)
    
    # Float metrics (1 decimal)
    for col in ['efficiency', 'distance', 'vo2max', 'spo2']:
        if col in data.columns:
            data[col] = data[col].round(1)
    
    # Add some missing data randomly (5% missing)
    for col in ['minutesAsleep', 'steps', 'heart_rate']:
        missing_mask = np.random.random(len(data)) < 0.05
        data.loc[missing_mask, col] = np.nan
    
    return data

def get_participant_type(participant_id):
    """Get participant type (OCD or Control)"""
    from config.settings import PARTICIPANT_PAIRS
    
    for pair_info in PARTICIPANT_PAIRS.values():
        if participant_id == pair_info["ocd"]:
            return "OCD"
        elif participant_id == pair_info["control"]:
            return "Control"
    
    return "Unknown"

def load_multiple_participants(participant_ids, date_range=None):
    """Load data for multiple participants and combine"""
    all_data = []
    
    for pid in participant_ids:
        data = load_participant_data(pid, date_range)
        all_data.append(data)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()

def get_data_summary(participant_id):
    """Get summary statistics for a participant"""
    data = load_participant_data(participant_id)
    
    summary = {
        'participant_id': participant_id,
        'participant_type': get_participant_type(participant_id),
        'total_records': len(data),
        'date_range': f"{data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}",
        'metrics': {}
    }
    
    # Calculate summary for each metric
    for col in ['minutesAsleep', 'steps', 'heart_rate', 'efficiency']:
        if col in data.columns:
            summary['metrics'][col] = {
                'mean': round(data[col].mean(), 1),
                'std': round(data[col].std(), 1),
                'min': round(data[col].min(), 1),
                'max': round(data[col].max(), 1),
                'missing': data[col].isna().sum()
            }
    
    return summary

