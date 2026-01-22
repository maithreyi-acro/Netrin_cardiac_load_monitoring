def compute_vo2_series(hr_corr, rest_hr, max_hr, vo2_max, vo2_rest=3.5):
    den = max_hr - rest_hr
    if den <= 0:
        return hr_corr * 0.0
    return vo2_rest + (hr_corr - rest_hr) * ((vo2_max - vo2_rest) / den)
