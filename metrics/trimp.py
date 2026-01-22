import numpy as np
from config.settings import TRIMP_SCALE, BANISTER_COEFF

def compute_hrr(hr_corr, rest_hr, max_hr):
    den = max_hr - rest_hr
    if den <= 0:
        return hr_corr * 0.0
    return ((hr_corr - rest_hr) / den).clip(0, 1)

def compute_trimp(hr_corr, rest_hr, max_hr, scale=TRIMP_SCALE):
    den = max_hr - rest_hr
    if den <= 0 or len(hr_corr) < 2:
        return 0.0
    hrr = ((hr_corr - rest_hr) / den).clip(0, 1)
    strain = hrr * np.exp(BANISTER_COEFF * hrr)
    t = hr_corr.index.view('int64') / 1e9
    dt_min = np.diff(t) / 60.0
    dt_min = np.append(dt_min, dt_min[-1])
    trimp = float(np.sum(strain.to_numpy() * dt_min))
    return trimp * scale

def compute_intensity(hr_corr, rest_hr, max_hr, scale=TRIMP_SCALE):
    training_load = compute_trimp(hr_corr, rest_hr, max_hr, scale)
    duration_min = (hr_corr.index[-1] - hr_corr.index[0]).total_seconds() / 60.0
    return training_load / duration_min if duration_min > 0 else 0.0
