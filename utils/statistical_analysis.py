"""
Statistical analysis utilities
"""
import pandas as pd
import numpy as np
from scipy import stats

def compare_participants(ocd_data, control_data, metrics):
    """
    Run statistical comparisons between OCD and Control participants
    """
    results = {
        'metrics': [],
        'summary': {}
    }
    
    for metric in metrics:
        if metric not in ocd_data.columns or metric not in control_data.columns:
            continue
        
        ocd_values = ocd_data[metric].dropna()
        control_values = control_data[metric].dropna()
        
        if len(ocd_values) < 3 or len(control_values) < 3:
            continue
        
        # T-test
        t_stat, p_value = stats.ttest_ind(ocd_values, control_values)
        
        # Effect size (Cohen's d)
        cohens_d = calculate_cohens_d(ocd_values, control_values)
        
        # Descriptive statistics
        result = {
            'metric': metric,
            'ocd_mean': round(ocd_values.mean(), 2),
            'ocd_std': round(ocd_values.std(), 2),
            'ocd_n': len(ocd_values),
            'control_mean': round(control_values.mean(), 2),
            'control_std': round(control_values.std(), 2),
            'control_n': len(control_values),
            'difference': round(ocd_values.mean() - control_values.mean(), 2),
            'percent_difference': round(((ocd_values.mean() - control_values.mean()) / control_values.mean()) * 100, 1),
            't_statistic': round(t_stat, 3),
            'p_value': round(p_value, 4),
            'cohens_d': round(cohens_d, 3),
            'significant': p_value < 0.05,
            'effect_size_interpretation': interpret_effect_size(cohens_d)
        }
        
        results['metrics'].append(result)
    
    # Overall summary
    significant_count = sum(1 for r in results['metrics'] if r['significant'])
    results['summary'] = {
        'total_metrics': len(results['metrics']),
        'significant_findings': significant_count,
        'percentage_significant': round((significant_count / len(results['metrics']) * 100) if results['metrics'] else 0, 1)
    }
    
    return results

def calculate_cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    
    # Pooled standard deviation
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    # Cohen's d
    d = (group1.mean() - group2.mean()) / pooled_std
    
    return d

def interpret_effect_size(cohens_d):
    """Interpret Cohen's d effect size"""
    abs_d = abs(cohens_d)
    
    if abs_d < 0.2:
        return "Negligible"
    elif abs_d < 0.5:
        return "Small"
    elif abs_d < 0.8:
        return "Medium"
    else:
        return "Large"

def calculate_correlation(data, metric1, metric2):
    """Calculate correlation between two metrics"""
    # Check if metrics exist
    if metric1 not in data.columns or metric2 not in data.columns:
        return None
    
    # Check if both are numeric
    if not pd.api.types.is_numeric_dtype(data[metric1]) or not pd.api.types.is_numeric_dtype(data[metric2]):
        return None
    
    clean_data = data[[metric1, metric2]].dropna()
    
    if len(clean_data) < 3:
        return None
    
    try:
        corr, p_value = stats.pearsonr(clean_data[metric1], clean_data[metric2])
        
        return {
            'correlation': round(float(corr), 3),
            'p_value': round(float(p_value), 4),
            'significant': p_value < 0.05,
            'interpretation': interpret_correlation(corr)
        }
    except (TypeError, ValueError):
        return None

def interpret_correlation(corr):
    """Interpret correlation coefficient"""
    abs_corr = abs(corr)
    
    if abs_corr < 0.1:
        return "Negligible"
    elif abs_corr < 0.3:
        return "Weak"
    elif abs_corr < 0.5:
        return "Moderate"
    elif abs_corr < 0.7:
        return "Strong"
    else:
        return "Very Strong"

def calculate_summary_statistics(data, metric):
    """Calculate comprehensive summary statistics for a metric"""
    # Check if metric exists in data
    if metric not in data.columns:
        return None
    
    # Check if data is numeric
    if not pd.api.types.is_numeric_dtype(data[metric]):
        return None
    
    values = data[metric].dropna()
    
    if len(values) == 0:
        return None
    
    try:
        return {
            'count': len(values),
            'mean': round(float(values.mean()), 2),
            'median': round(float(values.median()), 2),
            'std': round(float(values.std()), 2),
            'min': round(float(values.min()), 2),
            'max': round(float(values.max()), 2),
            'q25': round(float(values.quantile(0.25)), 2),
            'q75': round(float(values.quantile(0.75)), 2),
            'missing': int(data[metric].isna().sum()),
            'missing_percent': round((data[metric].isna().sum() / len(data)) * 100, 1)
        }
    except (TypeError, ValueError):
        # If any calculation fails, return None
        return None

