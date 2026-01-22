import numpy as np
import pandas as pd

def compute_acwr(summary_df):
    """
    Compute Acute:Chronic Workload Ratio (ACWR).
    
    Args:
        summary_df: DataFrame with session summaries
        
    Returns:
        pd.DataFrame: Summary with ACWR columns added
    """
    if summary_df.empty:
        return summary_df
    
    # Extract date and hour for grouping
    summary_df['date'] = summary_df['session'].astype(str).str[:8]
    # Safely extract hour, default to 0 if not available
    try:
        summary_df['hour'] = pd.to_numeric(summary_df['session'].astype(str).str[9:11], errors='coerce').fillna(0).astype(int)
    except:
        summary_df['hour'] = 0

    # Initialize ACWR columns
    summary_df['acute_load'] = summary_df['training_load']
    summary_df['chronic_load'] = summary_df['training_load']
    summary_df['acwr'] = 1.0

    # Compute ACWR
    for date, group in summary_df.groupby('date'):
        morning = group[group['hour'] < 12]
        evening = group[group['hour'] >= 12]

        if not morning.empty and not evening.empty:
            acute = morning['training_load'].sum()
            chronic = evening['training_load'].sum()
            acwr = acute / chronic if chronic != 0 else np.nan
            summary_df.loc[group.index, 'acute_load'] = round(acute, 3)
            summary_df.loc[group.index, 'chronic_load'] = round(chronic, 3)
            summary_df.loc[group.index, 'acwr'] = round(acwr, 3)
        elif not morning.empty and evening.empty:
            val = morning['training_load'].sum()
            summary_df.loc[group.index, ['acute_load','chronic_load']] = round(val, 3)
            summary_df.loc[group.index, 'acwr'] = 1.0
        elif morning.empty and not evening.empty:
            val = evening['training_load'].sum()
            summary_df.loc[group.index, ['acute_load','chronic_load']] = round(val, 3)
            summary_df.loc[group.index, 'acwr'] = 1.0

    # Drop helper columns
    summary_df = summary_df.drop(columns=['date','hour'])
    
    return summary_df
