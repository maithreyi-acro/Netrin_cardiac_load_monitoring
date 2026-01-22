import numpy as np

def compute_epoc_series(hr_series, rest_hr, max_hr, vo2max,
                        alpha_exp=1.92, k_base=0.12, k_vo2=0.06, min_hrr=0.10):
    den = max_hr - rest_hr
    if den <= 0:
        return 0.0, 0.0
    hrr = ((hr_series - rest_hr) / den).clip(0, 1)
    hrr_min = hrr.resample('60s').mean().fillna(0.0)
    inten = np.where(hrr_min >= min_hrr, hrr_min * np.exp(alpha_exp * hrr_min), 0.0)
    scale = (k_base + k_vo2 * (vo2max / 50.0))
    epoc_minute = scale * inten
    epoc_total = float(np.sum(epoc_minute))
    epoc_peak = float(np.max(epoc_minute)) if len(epoc_minute) else 0.0
    return round(epoc_total, 3), round(epoc_peak, 3)
