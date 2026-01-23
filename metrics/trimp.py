import numpy as np
from config.settings import TRIMP_SCALE, BANISTER_COEFF, BIN_SECONDS

def compute_hrr(hr_corr, rest_hr, max_hr):
    den = max_hr - rest_hr
    if den <= 0:
        return hr_corr * 0.0
    return ((hr_corr - rest_hr) / den).clip(0, 1)

def compute_trimp(hr_corr, rest_hr, max_hr, scale=TRIMP_SCALE):
    den = max_hr - rest_hr
    if den <= 0 or len(hr_corr) == 0:
        return 0.0
    hrr = ((hr_corr - rest_hr) / den).clip(0, 1)
    strain = hrr * np.exp(BANISTER_COEFF * hrr)
    dt_min = BIN_SECONDS / 60.0
    trimp = float(np.sum(strain.to_numpy()) * dt_min)
    return trimp * scale

def compute_intensity(hr_corr, rest_hr, max_hr, scale=TRIMP_SCALE):
    if len(hr_corr) == 0:
        return 0.0
    training_load = compute_trimp(hr_corr, rest_hr, max_hr, scale)
    duration_min = len(hr_corr) * (BIN_SECONDS / 60.0)
    return training_load / duration_min if duration_min > 0 else 0.0