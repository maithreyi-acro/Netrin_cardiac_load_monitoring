import os
import pandas as pd
from config.settings import DEFAULT_WEIGHT, DEFAULT_AGE
from metrics import (
    extract_hr, smooth_hr, compute_session_stats,
    compute_hrr, compute_trimp, compute_intensity,
    compute_hrv_from_hr_raw, compute_zones,
    compute_epoc_series, compute_vo2_series,
    compute_energy_expenditure, compute_movement_from_hr
)

def summarize_session(df, session_name, results_folder, weight=None, age=None):
    # Extract and preprocess HR
    hr_series = extract_hr(df)
    if hr_series.empty or len(hr_series) < 30:
        return None

    hr_corr = smooth_hr(hr_series, window_seconds=3)
    if hr_corr.empty:
        return None

    # Save corrected HR series
    save_path = os.path.join(results_folder, f"{session_name}_hr_corrected.csv")
    hr_corr.to_csv(save_path, index=True, header=["hr_corrected"])

    # Basic session stats
    avg_hr, max_hr, min_hr, rest_hr = compute_session_stats(hr_corr)

    # HRR
    hrr = compute_hrr(hr_corr, rest_hr, max_hr)

    # Duration
    duration_min = (hr_corr.index[-1] - hr_corr.index[0]).total_seconds() / 60.0
    if duration_min <= 0:
        return None

    # VO2max 
    vo2_max = 15.3 * (max_hr / rest_hr) if rest_hr > 0 else 0.0
    vo2_series = compute_vo2_series(hr_corr, rest_hr, max_hr, vo2_max)
    vo2 = float(vo2_series.mean())

    # EPOC
    epoc_total, epoc_peak = compute_epoc_series(hr_corr, rest_hr, max_hr, vo2_max)

    # Training load & intensity
    training_load = compute_trimp(hr_corr, rest_hr, max_hr)
    training_intensity = compute_intensity(hr_corr, rest_hr, max_hr)

    # HRV
    sdnn, rmssd, pnn50 = compute_hrv_from_hr_raw(hr_series)

    # Zones
    zones = compute_zones(hr_corr, hrr)

    # Energy expenditure - logistic model
    ee_series = compute_energy_expenditure(hr_corr)
    ee_men = float(ee_series.mean())

    # Movement load
    movement_load, movement_load_intensity = compute_movement_from_hr(hr_corr, rest_hr)

    return {
        "session": session_name,
        "avg_hr": round(avg_hr, 2),
        "min_hr": round(min_hr, 2),
        "max_hr": round(max_hr, 2),
        "rest_hr": round(rest_hr, 2),
        "training_load": round(training_load, 3),
        "training_intensity": round(training_intensity, 3),
        "sdnn": round(sdnn, 2),
        "rmssd": round(rmssd, 2),
        "pnn50": round(pnn50, 2),
        "epoc_total": round(epoc_total, 3),
        "epoc_peak": round(epoc_peak, 3),
        "ee_men": round(ee_men, 2),
        "vo2": round(vo2, 2),
        "vo2_max": round(vo2_max, 2),
        "movement_load": round(movement_load, 2),
        "movement_load_intensity": round(movement_load_intensity, 2),
        **zones
    }
