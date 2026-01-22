import numpy as np
import pandas as pd
from config.settings import HR_FLOOR, HR_CAP

def compute_hrv_from_hr_raw(hr_series, gap_limit=3):
    hr = pd.to_numeric(hr_series, errors='coerce').clip(lower=HR_FLOOR, upper=HR_CAP).dropna()
    hr_1hz = (
        hr.resample('1s')
        .median()
        .interpolate('linear', limit=gap_limit)
        .clip(lower=HR_FLOOR, upper=HR_CAP)
        .dropna()
    )
    if len(hr_1hz) == 0:
         return 0.0, 0.0, 0.0
         
    rr = 60000.0 / hr_1hz.to_numpy()
    rr = rr[(rr >= 250.0) & (rr <= 2500.0)]
    if len(rr) < 2:
        return 0.0, 0.0, 0.0
    sdnn = float(np.std(rr, ddof=1))
    drr = np.diff(rr)
    rmssd = float(np.sqrt(np.mean(drr**2))) if len(drr) > 0 else 0.0
    pnn50 = float((np.sum(np.abs(drr) > 50.0) / len(drr)) * 100.0) if len(drr) > 0 else 0.0
    return sdnn, rmssd, pnn50
