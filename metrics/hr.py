import pandas as pd
import numpy as np
from config.settings import HR_FLOOR, HR_CAP, BIN_SECONDS, SMOOTH_WINDOW_SEC, INTERP_LIMIT_SEC

def extract_hr(df):
    if not {'timestamp', 'value'}.issubset(df.columns):
        return pd.Series(dtype=float)

    if 'data_item' in df.columns:
        hr_rows = df[df['data_item'].astype(str).str.lower() == 'hr'].copy()
        if hr_rows.empty:
            hr_rows = df.copy()
    else:
        hr_rows = df.copy()

    hr_rows['timestamp'] = pd.to_datetime(
        hr_rows['timestamp'], errors='coerce', utc=True
    )
    hr_rows['value'] = pd.to_numeric(hr_rows['value'], errors='coerce')

    hr_rows = (
        hr_rows
        .dropna(subset=['timestamp', 'value'])
        .sort_values('timestamp')
    )

    return hr_rows.set_index('timestamp')['value']

def smooth_hr(hr_series, window_seconds=SMOOTH_WINDOW_SEC, gap_limit_seconds=INTERP_LIMIT_SEC):
    hr_series = pd.to_numeric(hr_series, errors='coerce').dropna()

    hr_3s = (
        hr_series
        .resample(f'{BIN_SECONDS}s')
        .mean()
        .clip(lower=HR_FLOOR, upper=HR_CAP)
    )

    max_bins = max(1, gap_limit_seconds // BIN_SECONDS)
    hr_3s = hr_3s.interpolate(
        method='linear',
        limit=max_bins,
        limit_direction='forward'
    )

    window_bins = max(1, window_seconds // BIN_SECONDS)
    hr_smoothed = hr_3s.rolling(
        window=window_bins,
        center=True,
        min_periods=window_bins
    ).mean()

    return hr_smoothed.dropna()

def compute_session_stats(hr_corr):
    if len(hr_corr) == 0:
        return 0.0, 0.0, 0.0, 0.0

    avg_hr = float(hr_corr.mean())
    min_hr = float(np.percentile(hr_corr, 1))
    max_hr = float(np.percentile(hr_corr, 95))
    rest_hr = min_hr

    return avg_hr, max_hr, min_hr, rest_hr

def compute_session_stats(hr_corr, hr_max_ref):
    if len(hr_corr) == 0:
        return {
            "avg_hr": 0.0,
            "max_hr": 0.0,
            "min_hr": 0.0,
            "rest_hr": 0.0,
            "avg_hr_pct": 0.0,
            "max_hr_pct": 0.0,
            "min_hr_pct": 0.0,
        }

    avg_hr = float(hr_corr.mean())
    min_hr = float(np.percentile(hr_corr, 5))
    max_hr = float(np.percentile(hr_corr, 95))
    rest_hr = min_hr

    avg_hr_pct = (avg_hr / hr_max_ref) * 100
    max_hr_pct = (max_hr / hr_max_ref) * 100
    min_hr_pct = (min_hr / hr_max_ref) * 100

    return {
        "avg_hr": avg_hr,
        "max_hr": max_hr,
        "min_hr": min_hr,
        "rest_hr": rest_hr,
        "avg_hr_pct": avg_hr_pct,
        "max_hr_pct": max_hr_pct,
        "min_hr_pct": min_hr_pct,
    }