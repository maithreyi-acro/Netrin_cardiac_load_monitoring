import pandas as pd

def load_summary(csv_path):
    df = pd.read_csv(csv_path)

    # Parse session date from session name (format: YYYYMMDD_HHMMSS)
    df["session_date"] = pd.to_datetime(
        df["session"].astype(str).str[:8],
        format="%Y%m%d",
        errors='coerce'
    )
    
    # Create week and month aggregations
    df["week"] = df["session_date"].dt.to_period("W").dt.start_time
    df["month"] = df["session_date"].dt.to_period("M").dt.start_time

    return df.sort_values("session_date").reset_index(drop=True)
