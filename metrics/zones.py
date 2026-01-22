import numpy as np
from config.settings import ZONE_BOUNDS

def compute_zones(hr_corr, hrr):
    arr = hrr.to_numpy()
    time_diff_ms = np.diff(hr_corr.index.values.astype('datetime64[ms]')).astype(int)
    time_diff_ms = np.append(time_diff_ms, time_diff_ms[-1])
    out = {}
    total_time = time_diff_ms.sum()
    for i, (low, high) in enumerate(ZONE_BOUNDS):
        mask = (arr >= low) & (arr < high) if i < len(ZONE_BOUNDS)-1 else (arr >= low) & (arr <= high)
        duration = int(time_diff_ms[mask].sum())
        out[f"zone_{i}_d"] = duration
        out[f"zone_{i}_pct"] = round((duration / total_time) * 100, 2) if total_time > 0 else 0.0
    return out
