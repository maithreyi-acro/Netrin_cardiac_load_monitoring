import numpy as np

def compute_energy_expenditure(hr_series, phi1=15.0, phi2=120.0, phi3=15.0):
    hr_array = np.array(hr_series, dtype=float)
    ee_series = phi1 / (1.0 + np.exp((phi2 - hr_array) / phi3))

    return ee_series