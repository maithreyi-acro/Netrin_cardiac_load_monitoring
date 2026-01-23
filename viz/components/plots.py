from viz.plots.hrv_plots import (
    create_hrv_rmssd_plotly, create_hrv_sdnn_plotly, create_hrv_pnn50_plotly
)
from viz.plots.load_plots import (
    create_training_load_plotly, create_load_intensity_plotly,
    create_acwr_plotly, create_acute_chronic_plotly
)
from viz.plots.cardiac_plots import (
    create_resting_hr_plotly, create_avg_hr_plotly,
    create_max_hr_plotly, create_min_hr_plotly
)
from viz.plots.metabolic_plots import (
    create_epoc_total_plotly, create_epoc_peak_plotly,
    create_vo2_plotly, create_vo2max_plotly, create_energy_plotly
)
from viz.plots.movement_plots import (
    create_movement_load_plotly, create_movement_intensity_plotly
)
from viz.plots.zone_plots import (
    create_zones_stacked_plotly, create_zones_pie_plotly, create_zones_heatmap_plotly
)
from viz.plots.metrics_tab_plots import (
    create_hrv_recovery_trend, create_load_vs_hrv_trend, create_weekly_hr_metrics,
    create_weekly_zone_split, create_avg_training_load_line, create_weekly_acwr_line,
    create_session_time_hrv_load, create_session_quality_graph
)

def create_hrv_plots(df_filtered):
    return (
        create_hrv_rmssd_plotly(df_filtered),
        create_hrv_sdnn_plotly(df_filtered),
        create_hrv_pnn50_plotly(df_filtered)
    )

def create_load_plots(df_filtered):
    return (
        create_training_load_plotly(df_filtered),
        create_load_intensity_plotly(df_filtered),
        create_acwr_plotly(df_filtered),
        create_acute_chronic_plotly(df_filtered)
    )

def create_hr_plots(df_filtered):
    return (
        create_resting_hr_plotly(df_filtered),
        create_avg_hr_plotly(df_filtered),
        create_max_hr_plotly(df_filtered),
        create_min_hr_plotly(df_filtered)
    )

def create_metabolic_plots(df_filtered):
    return (
        create_epoc_total_plotly(df_filtered),
        create_epoc_peak_plotly(df_filtered),
        create_vo2_plotly(df_filtered),
        create_vo2max_plotly(df_filtered),
        create_energy_plotly(df_filtered)
    )

def create_movement_plots(df_filtered):
    return (
        create_movement_load_plotly(df_filtered),
        create_movement_intensity_plotly(df_filtered)
    )

def create_zone_plots(df_filtered):
    return (
        create_zones_stacked_plotly(df_filtered),
        create_zones_pie_plotly(df_filtered),
        create_zones_heatmap_plotly(df_filtered)
    )

def create_metrics_tab_plots(df_filtered):
    return (
        create_hrv_recovery_trend(df_filtered),
        create_load_vs_hrv_trend(df_filtered),
        create_weekly_hr_metrics(df_filtered, "Readiness"),
        create_weekly_hr_metrics(df_filtered, "Training"),
        create_weekly_zone_split(df_filtered),
        create_avg_training_load_line(df_filtered),
        create_weekly_acwr_line(df_filtered),
        create_session_time_hrv_load(df_filtered, "Morning"),
        create_session_time_hrv_load(df_filtered, "Afternoon and Evening"),
        create_session_quality_graph(df_filtered)
    )
