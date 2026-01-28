import os

# Path to raw data (zip files)
RAW_DATA_DIR = os.path.join("bin", "raw")

# Heart Rate Constraints
HR_FLOOR = 40       
HR_CAP = 210        
BIN_SECONDS = 3
BIN_MINUTES = BIN_SECONDS / 60.0 

# Preprocessing
INTERP_LIMIT_SEC = 10
SMOOTH_WINDOW_SEC = 9

# Training load
BANISTER_COEFF = 1.90
TRIMP_SCALE = 0.64

# Zones
ZONE_BOUNDS = [(0.0,0.5),(0.5,0.6),(0.6,0.7),(0.7,0.8),(0.8,0.9),(0.9,1.0)]
     
