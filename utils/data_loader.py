"""
Data loading utilities for Fitbit data
Supports loading from AWS S3 (real data) with fallback to sample data
"""
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np

# Try to import S3 loader
try:
    from utils.s3_loader import (
        load_participant_data_from_s3,
        get_s3_participants,
        is_s3_available
    )
    S3_AVAILABLE = True
except ImportError:
    S3_AVAILABLE = False

# Flag to control data source (can be toggled in the app)
USE_S3_DATA = True  # Set to False to use sample data


def get_available_participants():
    """Get list of all available participants"""
    
    # Try S3 first if enabled
    if USE_S3_DATA and S3_AVAILABLE:
        try:
            s3_participants = get_s3_participants()
            if s3_participants["ocd"] or s3_participants["ctrl"]:
                participants = []
                
                # Add OCD participants
                for pid in s3_participants["ocd"]:
                    participants.append({
                        "id": pid,
                        "type": "OCD",
                        "pair_id": None,  # Pairs not defined in S3
                        "source": "s3"
                    })
                
                # Add Control participants
                for pid in s3_participants["ctrl"]:
                    participants.append({
                        "id": pid,
                        "type": "Control",
                        "pair_id": None,
                        "source": "s3"
                    })
                
                return participants
        except Exception as e:
            print(f"S3 loading failed, falling back to sample data: {e}")
    
    # Fallback to hardcoded sample data
    from config.settings import PARTICIPANT_PAIRS
    
    participants = []
    for pair_id, pair_info in PARTICIPANT_PAIRS.items():
        participants.append({
            "id": pair_info["ocd"],
            "type": "OCD",
            "pair_id": pair_id,
            "source": "sample"
        })
        participants.append({
            "id": pair_info["control"],
            "type": "Control",
            "pair_id": pair_id,
            "source": "sample"
        })
    
    return participants


def get_participant_pairs():
    """Get list of participant pairs"""
    
    # For S3 data, we don't have predefined pairs
    # Return pairs from settings if available
    from config.settings import PARTICIPANT_PAIRS
    
    pairs = []
    for pair_id, pair_info in PARTICIPANT_PAIRS.items():
        pairs.append({
            "pair_id": pair_id,
            "ocd_id": pair_info["ocd"],
            "control_id": pair_info["control"],
            "ocd_record_count": 90,  # Will be updated when data is loaded
            "control_record_count": 90,
            "ocd_date_range": "Variable",
            "control_date_range": "Variable"
        })
    
    return pairs


def load_participant_data(participant_id, date_range=None):
    """
    Load data for a specific participant
    Tries S3 first, falls back to sample data
    """
    
    # Try S3 first if enabled
    if USE_S3_DATA and S3_AVAILABLE:
        try:
            s3_data = load_participant_data_from_s3(participant_id, date_range)
            if s3_data is not None and not s3_data.empty:
                return s3_data
        except Exception as e:
            print(f"S3 loading failed for {participant_id}, using sample data: {e}")
    
    # Fallback to generated sample data
    return _generate_sample_data(participant_id, date_range)


def _generate_sample_data(participant_id, date_range=None):
    """
    Generate sample data for demonstration (fallback when S3 unavailable)
    """
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
        'distance': np.random.normal(base_steps / 2000, steps_std / 2000, len(dates)).clip(0.5, 15),
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
    for col in ['minutesAsleep', 'minutesAwake', 'timeInBed', 'minutesToFallAsleep', 
                'minutesAfterWakeup', 'steps', 'calories', 'floors', 'activeMinutes', 
                'heart_rate', 'breathingRate']:
        if col in data.columns:
            data[col] = data[col].round(0).astype(int)
    
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
    
    # Check S3 participants first
    if USE_S3_DATA and S3_AVAILABLE:
        try:
            s3_participants = get_s3_participants()
            if participant_id in s3_participants["ocd"]:
                return "OCD"
            elif participant_id in s3_participants["ctrl"]:
                return "Control"
        except Exception:
            pass
    
    # Fallback to settings
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
        if data is not None and not data.empty:
            all_data.append(data)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    
    return pd.DataFrame()


def get_data_summary(participant_id):
    """Get summary statistics for a participant"""
    data = load_participant_data(participant_id)
    
    if data is None or data.empty:
        return {
            'participant_id': participant_id,
            'participant_type': get_participant_type(participant_id),
            'total_records': 0,
            'date_range': "No data",
            'metrics': {},
            'source': 'none'
        }
    
    # Determine data source
    source = 'sample'
    if USE_S3_DATA and S3_AVAILABLE:
        try:
            s3_participants = get_s3_participants()
            if participant_id in s3_participants["ocd"] or participant_id in s3_participants["ctrl"]:
                source = 's3'
        except Exception:
            pass
    
    summary = {
        'participant_id': participant_id,
        'participant_type': get_participant_type(participant_id),
        'total_records': len(data),
        'date_range': f"{data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}" if 'date' in data.columns else "Unknown",
        'metrics': {},
        'source': source
    }
    
    # Calculate summary for each metric
    for col in ['minutesAsleep', 'steps', 'heart_rate', 'efficiency']:
        if col in data.columns:
            summary['metrics'][col] = {
                'mean': round(data[col].mean(), 1) if not data[col].isna().all() else None,
                'std': round(data[col].std(), 1) if not data[col].isna().all() else None,
                'min': round(data[col].min(), 1) if not data[col].isna().all() else None,
                'max': round(data[col].max(), 1) if not data[col].isna().all() else None,
                'missing': int(data[col].isna().sum())
            }
    
    return summary


def get_data_source_status():
    """
    Get current data source status
    Returns dict with source info
    """
    status = {
        'use_s3': USE_S3_DATA,
        's3_module_available': S3_AVAILABLE,
        's3_connected': False,
        'source': 'sample'
    }
    
    if USE_S3_DATA and S3_AVAILABLE:
        try:
            from utils.s3_loader import is_s3_available
            status['s3_connected'] = is_s3_available()
            if status['s3_connected']:
                status['source'] = 's3'
        except Exception:
            pass
    
    return status
