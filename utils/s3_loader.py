"""
AWS S3 Data Loader for Fitbit Data
Loads real participant data from S3 bucket: testfitbitocd
"""
import boto3
import pandas as pd
from io import StringIO
import streamlit as st
from typing import Optional, List, Dict
import os


# S3 Configuration
S3_BUCKET = "testfitbitocd"
S3_REGION = "us-west-2"

# Data folders in S3
DATA_FOLDERS = {
    "sleep_meta": "sleep-meta",
    "sleep": "sleep",
    "daily": "daily",
    "heart": "heart",
    "steps": "steps",
    "breath": "breath",
    "spo2": "spo2",
    "hrv": "hrv",
    "skin": "skin",
}


def get_s3_client():
    """
    Get S3 client using credentials from Streamlit secrets or environment variables
    """
    try:
        # Try Streamlit secrets first (for deployed app)
        if hasattr(st, 'secrets') and 'aws' in st.secrets:
            return boto3.client(
                's3',
                aws_access_key_id=st.secrets['aws']['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=st.secrets['aws']['AWS_SECRET_ACCESS_KEY'],
                region_name=st.secrets['aws'].get('AWS_DEFAULT_REGION', S3_REGION)
            )
    except Exception:
        pass
    
    # Try environment variables
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    if access_key and secret_key:
        return boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=os.environ.get('AWS_DEFAULT_REGION', S3_REGION)
        )
    
    # Try default AWS profile
    try:
        return boto3.client('s3', region_name=S3_REGION)
    except Exception as e:
        st.error(f"Failed to connect to AWS S3: {e}")
        return None


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_s3_participants() -> Dict[str, List[str]]:
    """
    Get list of all participants from S3 (ALL CAPS folders only)
    Returns dict with 'ocd' and 'ctrl' lists
    """
    s3 = get_s3_client()
    if not s3:
        return {"ocd": [], "ctrl": []}
    
    participants = {"ocd": [], "ctrl": []}
    
    try:
        # Get OCD participants
        response = s3.list_objects_v2(
            Bucket=S3_BUCKET, 
            Prefix='ocd/', 
            Delimiter='/'
        )
        for prefix in response.get('CommonPrefixes', []):
            folder_name = prefix['Prefix'].split('/')[1]
            if folder_name.isupper():  # Only ALL CAPS folders
                participants["ocd"].append(folder_name)
        
        # Get Control participants
        response = s3.list_objects_v2(
            Bucket=S3_BUCKET, 
            Prefix='ctrl/', 
            Delimiter='/'
        )
        for prefix in response.get('CommonPrefixes', []):
            folder_name = prefix['Prefix'].split('/')[1]
            if folder_name.isupper():  # Only ALL CAPS folders
                participants["ctrl"].append(folder_name)
                
    except Exception as e:
        st.warning(f"Could not fetch participants from S3: {e}")
    
    return participants


def _get_participant_prefix(participant_id: str) -> Optional[str]:
    """
    Determine if participant is OCD or Control and return S3 prefix
    """
    participants = get_s3_participants()
    
    if participant_id in participants["ocd"]:
        return f"ocd/{participant_id}"
    elif participant_id in participants["ctrl"]:
        return f"ctrl/{participant_id}"
    
    return None


def _read_s3_csv(s3_client, key: str) -> Optional[pd.DataFrame]:
    """
    Read a CSV file from S3 and return as DataFrame
    """
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
        content = obj['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(content))
    except Exception as e:
        return None


def _list_s3_files(s3_client, prefix: str) -> List[str]:
    """
    List all files in an S3 prefix
    """
    files = []
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
            for obj in page.get('Contents', []):
                files.append(obj['Key'])
    except Exception:
        pass
    return files


@st.cache_data(ttl=3600)
def load_sleep_meta_from_s3(participant_id: str) -> Optional[pd.DataFrame]:
    """
    Load sleep metadata for a participant from S3
    """
    s3 = get_s3_client()
    if not s3:
        return None
    
    prefix = _get_participant_prefix(participant_id)
    if not prefix:
        return None
    
    sleep_meta_prefix = f"{prefix}/sleep-meta/"
    files = _list_s3_files(s3, sleep_meta_prefix)
    
    all_data = []
    for file_key in files:
        df = _read_s3_csv(s3, file_key)
        if df is not None and not df.empty:
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        # Clean up and standardize
        if 'dateTime' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateTime'], errors='coerce')
        elif 'dateOfSleep' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateOfSleep'], errors='coerce')
        return combined.drop_duplicates(subset=['date'] if 'date' in combined.columns else None)
    
    return None


@st.cache_data(ttl=3600)
def load_daily_from_s3(participant_id: str) -> Optional[pd.DataFrame]:
    """
    Load daily activity data (steps, calories, active minutes) from S3
    """
    s3 = get_s3_client()
    if not s3:
        return None
    
    prefix = _get_participant_prefix(participant_id)
    if not prefix:
        return None
    
    daily_prefix = f"{prefix}/daily/"
    files = _list_s3_files(s3, daily_prefix)
    
    all_data = []
    for file_key in files:
        df = _read_s3_csv(s3, file_key)
        if df is not None and not df.empty:
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        if 'dateTime' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateTime'], errors='coerce')
        return combined.drop_duplicates(subset=['date'] if 'date' in combined.columns else None)
    
    return None


@st.cache_data(ttl=3600)
def load_steps_from_s3(participant_id: str) -> Optional[pd.DataFrame]:
    """
    Load steps data from S3
    """
    s3 = get_s3_client()
    if not s3:
        return None
    
    prefix = _get_participant_prefix(participant_id)
    if not prefix:
        return None
    
    steps_prefix = f"{prefix}/steps/"
    files = _list_s3_files(s3, steps_prefix)
    
    all_data = []
    for file_key in files:
        df = _read_s3_csv(s3, file_key)
        if df is not None and not df.empty:
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        if 'dateTime' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateTime'], errors='coerce')
            combined['steps'] = combined['value']
        return combined.drop_duplicates(subset=['date'] if 'date' in combined.columns else None)
    
    return None


@st.cache_data(ttl=3600)
def load_heart_daily_from_s3(participant_id: str) -> Optional[pd.DataFrame]:
    """
    Load heart rate data and aggregate to daily averages
    """
    s3 = get_s3_client()
    if not s3:
        return None
    
    prefix = _get_participant_prefix(participant_id)
    if not prefix:
        return None
    
    heart_prefix = f"{prefix}/heart/"
    files = _list_s3_files(s3, heart_prefix)
    
    all_data = []
    for file_key in files:
        df = _read_s3_csv(s3, file_key)
        if df is not None and not df.empty:
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        if 'dateTime' in combined.columns and 'value' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateTime'], errors='coerce')
            # Aggregate to daily average heart rate
            daily_hr = combined.groupby('date')['value'].mean().reset_index()
            daily_hr.columns = ['date', 'heart_rate']
            return daily_hr
    
    return None


@st.cache_data(ttl=3600)
def load_breath_from_s3(participant_id: str) -> Optional[pd.DataFrame]:
    """
    Load breathing rate data from S3
    """
    s3 = get_s3_client()
    if not s3:
        return None
    
    prefix = _get_participant_prefix(participant_id)
    if not prefix:
        return None
    
    breath_prefix = f"{prefix}/breath/"
    files = _list_s3_files(s3, breath_prefix)
    
    all_data = []
    for file_key in files:
        df = _read_s3_csv(s3, file_key)
        if df is not None and not df.empty:
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        if 'dateTime' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateTime'], errors='coerce')
            # Use fullSleepSummary as breathing rate
            if 'fullSleepSummary' in combined.columns:
                combined['breathingRate'] = combined['fullSleepSummary']
        return combined.drop_duplicates(subset=['date'] if 'date' in combined.columns else None)
    
    return None


@st.cache_data(ttl=3600)
def load_spo2_daily_from_s3(participant_id: str) -> Optional[pd.DataFrame]:
    """
    Load SpO2 data and aggregate to daily averages
    """
    s3 = get_s3_client()
    if not s3:
        return None
    
    prefix = _get_participant_prefix(participant_id)
    if not prefix:
        return None
    
    spo2_prefix = f"{prefix}/spo2/"
    files = _list_s3_files(s3, spo2_prefix)
    
    all_data = []
    for file_key in files:
        df = _read_s3_csv(s3, file_key)
        if df is not None and not df.empty:
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        if 'dateTime' in combined.columns and 'value' in combined.columns:
            combined['date'] = pd.to_datetime(combined['dateTime'], errors='coerce')
            # Aggregate to daily average SpO2
            daily_spo2 = combined.groupby('date')['value'].mean().reset_index()
            daily_spo2.columns = ['date', 'spo2']
            return daily_spo2
    
    return None


@st.cache_data(ttl=3600)
def load_participant_data_from_s3(participant_id: str, date_range=None) -> Optional[pd.DataFrame]:
    """
    Load and combine all data types for a participant from S3
    Returns a DataFrame with daily metrics matching the app's expected format
    """
    # Load all data types
    sleep_meta = load_sleep_meta_from_s3(participant_id)
    daily_data = load_daily_from_s3(participant_id)
    steps_data = load_steps_from_s3(participant_id)
    heart_data = load_heart_daily_from_s3(participant_id)
    breath_data = load_breath_from_s3(participant_id)
    spo2_data = load_spo2_daily_from_s3(participant_id)
    
    # Start with sleep meta as base (has most sleep metrics)
    if sleep_meta is not None and not sleep_meta.empty:
        combined = sleep_meta.copy()
    else:
        # If no sleep data, try to use daily data as base
        if daily_data is not None and not daily_data.empty:
            combined = daily_data[['date']].copy() if 'date' in daily_data.columns else pd.DataFrame()
        else:
            return None
    
    # Ensure date column exists
    if 'date' not in combined.columns:
        return None
    
    # Merge daily activity data
    if daily_data is not None and 'date' in daily_data.columns:
        # Select relevant columns
        daily_cols = ['date', 'steps', 'caloriesOut', 'fairlyActiveMinutes', 
                      'lightlyActiveMinutes', 'veryActiveMinutes', 'sedentaryMinutes',
                      'restingHeartRate']
        available_cols = [c for c in daily_cols if c in daily_data.columns]
        if available_cols:
            combined = combined.merge(
                daily_data[available_cols], 
                on='date', 
                how='outer',
                suffixes=('', '_daily')
            )
    
    # Merge steps if not already present
    if steps_data is not None and 'date' in steps_data.columns:
        if 'steps' not in combined.columns:
            combined = combined.merge(
                steps_data[['date', 'steps']], 
                on='date', 
                how='outer'
            )
    
    # Merge heart rate
    if heart_data is not None and 'date' in heart_data.columns:
        combined = combined.merge(heart_data, on='date', how='outer')
    
    # Merge breathing rate
    if breath_data is not None and 'date' in breath_data.columns:
        if 'breathingRate' in breath_data.columns:
            combined = combined.merge(
                breath_data[['date', 'breathingRate']], 
                on='date', 
                how='outer'
            )
    
    # Merge SpO2
    if spo2_data is not None and 'date' in spo2_data.columns:
        combined = combined.merge(spo2_data, on='date', how='outer')
    
    # Add participant info
    participants = get_s3_participants()
    if participant_id in participants["ocd"]:
        combined['participant_type'] = 'OCD'
    else:
        combined['participant_type'] = 'Control'
    
    combined['participantId'] = participant_id
    
    # Rename columns to match expected format
    column_mapping = {
        'caloriesOut': 'calories',
        'restingHeartRate': 'heart_rate',
        'veryActiveMinutes': 'activeMinutes',
    }
    combined = combined.rename(columns=column_mapping)
    
    # If heart_rate not present but we have it from heart data
    if 'heart_rate' not in combined.columns and heart_data is not None:
        pass  # Already merged above
    
    # Filter by date range if provided
    if date_range and 'date' in combined.columns:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        combined = combined[
            (combined['date'] >= start_date) & 
            (combined['date'] <= end_date)
        ]
    
    # Sort by date
    if 'date' in combined.columns:
        combined = combined.sort_values('date').reset_index(drop=True)
    
    return combined


def is_s3_available() -> bool:
    """
    Check if S3 connection is available
    """
    s3 = get_s3_client()
    if not s3:
        return False
    
    try:
        # Try a simple list operation
        s3.list_objects_v2(Bucket=S3_BUCKET, MaxKeys=1)
        return True
    except Exception:
        return False

