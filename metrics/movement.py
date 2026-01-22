import numpy as np
from config.settings import BIN_MINUTES

def compute_movement_from_hr(hr_corr, rest_hr):
    hr_excess = (hr_corr - rest_hr).clip(lower=0)
    dt_min = BIN_MINUTES
    movement_load = float(np.sum(hr_excess.to_numpy()) * dt_min)
    duration_min = (hr_corr.index[-1] - hr_corr.index[0]).total_seconds() / 60.0
    movement_load_intensity = movement_load / duration_min if duration_min > 0 else 0.0
    return movement_load, movement_load_intensity
