# Cardiac Load Monitoring Platform

## Overview
A complete pipeline for processing cardiac session data, computing performance metrics, and visualizing insights through an interactive dashboard.

## Architecture

```
Raw Data → Metrics Computation → Metrics Dataset → Visualization → Dashboard
```

## Project Structure
```
cardiac-load-monitoring/
├── main.py                     # Metrics computation pipeline
├── app.py                      # Dashboard web application (entry point)
├── run_dashboard.py            # Quick launcher
├── config/
│   └── settings.py             # Centralized constants
├── utils/
│   └── file_io.py              # File I/O utilities
├── metrics/                    # Metric calculation modules
│   ├── hr.py
│   ├── trimp.py
│   ├── hrv.py
│   ├── zones.py
│   ├── epoc.py
│   ├── vo2.py
│   ├── energy.py
│   └── movement.py
├── pipeline/                   # Orchestration logic
│   ├── summarize.py
│   └── acwr.py
├── viz/                        # Visualization layer
│   ├── data/
│   │   └── load_data.py        # Data loader
│   ├── components/             # Dashboard components
│   │   ├── layout.py           # UI layout
│   │   ├── plots.py            # Plot generators
│   │   └── callbacks.py        # Interactivity
│   └── plots/                  # Seaborn plot modules (optional)
└── bin/
    ├── raw/                    # Input: zip files with HR data
    └── processed/              # Output: metrics CSV
```

## Workflow

### 1. Compute Metrics
Process raw HR data and calculate all metrics:
```bash
python main.py
```

**Input:** `bin/raw/*.zip` (containing `hr.csv` and `summary.csv`)  
**Output:** `bin/processed/hr_summary.csv`

### 2. Launch Dashboard
Visualize computed metrics:
```bash
python app.py
```
Or use the launcher:
```bash
python run_dashboard.py
```


**Metric Categories:**
-  **HRV Metrics**: RMSSD, SDNN, pNN50
-  **Training Load**: Load, Intensity, ACWR, Acute/Chronic
-  **Heart Rate**: Resting, Average, Max, Min
-  **Metabolic**: EPOC, VO₂, VO₂ Max, Energy Expenditure
-  **Movement**: Load, Intensity
-  **HR Zones**: Distribution, Heatmap, Pie Chart


