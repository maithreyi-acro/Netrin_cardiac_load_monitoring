import os
from dash import Input, Output, html
from viz.data.load_data import load_summary
from .plots import (
    create_hrv_plots, create_load_plots, create_hr_plots,
    create_metabolic_plots, create_movement_plots, create_zone_plots,
    create_metrics_tab_plots
)
from .layout import create_summary_cards

def register_callbacks(app, processed_dir):
    @app.callback(
        [Output('summary-cards-container', 'children'),
         Output('hrv-rmssd', 'figure'), Output('hrv-sdnn', 'figure'), Output('hrv-pnn50', 'figure'),
         Output('training-load', 'figure'), Output('load-intensity', 'figure'),
         Output('acwr-trend', 'figure'), Output('acute-chronic', 'figure'),
         Output('rest-hr', 'figure'), Output('avg-hr', 'figure'), 
         Output('max-hr', 'figure'), Output('min-hr', 'figure'),
         Output('epoc-total', 'figure'), Output('epoc-peak', 'figure'),
         Output('vo2', 'figure'), Output('vo2-max', 'figure'), Output('energy-exp', 'figure'),
         Output('movement-load', 'figure'), Output('movement-intensity', 'figure'),
         Output('zones-stacked', 'figure'), Output('zones-pie', 'figure'), 
         Output('zones-heatmap', 'figure'),
         Output('hrv-recovery-trend', 'figure'), Output('load-vs-hrv-trend', 'figure'),
         Output('hr-metrics-readiness', 'figure'), Output('hr-metrics-training', 'figure'),
         Output('weekly-zone-split', 'figure'), Output('avg-load-line', 'figure'),
         Output('weekly-acwr-line', 'figure'), Output('morning-hrv-load', 'figure'),
         Output('evening-hrv-load', 'figure'), Output('session-quality-graph', 'figure')],
        [Input('athlete-select', 'value'),
         Input('date-range', 'value')]
    )
    def update_dashboard(athlete, days):
        if not athlete:
            return [html.Div()] + [{} for _ in range(31)]
            
        csv_path = os.path.join(processed_dir, f"hr_summary_{athlete}.csv")
        if not os.path.exists(csv_path):
            # Fallback to general summary if specific one doesn't exist
            csv_path = os.path.join(processed_dir, "hr_summary.csv")
            
        try:
            df = load_summary(csv_path)
            df_filtered = df.tail(days)
            
            # Generate summary cards
            summary_cards = create_summary_cards(df_filtered)
            
            # Generate all plots
            hrv_plots = create_hrv_plots(df_filtered)
            load_plots = create_load_plots(df_filtered)
            hr_plots = create_hr_plots(df_filtered)
            metabolic_plots = create_metabolic_plots(df_filtered)
            movement_plots = create_movement_plots(df_filtered)
            zone_plots = create_zone_plots(df_filtered)
            metrics_plots = create_metrics_tab_plots(df_filtered)
            
            return (summary_cards, *hrv_plots, *load_plots, *hr_plots, *metabolic_plots, 
                    *movement_plots, *zone_plots, *metrics_plots)
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
            return [html.Div(f"Error: {str(e)}")] + [{} for _ in range(31)]
