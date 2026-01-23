import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_hrv_recovery_trend(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=df['session_date'], y=df['rmssd'], name="HRV (RMSSD)",
                  line=dict(color='#f1c40f', width=2), mode='lines+markers'),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=df['session_date'], y=df['recovery_beats'], name="Recovery Beats",
                  line=dict(color='#3498db', width=2), mode='lines+markers'),
        secondary_y=True,
    )
    
    fig.update_layout(title="Heart Rate and Recovery Metrics", xaxis_title="Date",
                      template='plotly_white', height=500)
    fig.update_yaxes(title_text="HRV", secondary_y=False)
    fig.update_yaxes(title_text="Recovery Beats per 60s", secondary_y=True)
    return fig

def create_load_vs_hrv_trend(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['session_date'], y=df['training_load'], name="Training Load",
                         marker_color='#e67e22', opacity=0.6))
    fig.add_trace(go.Scatter(x=df['session_date'], y=df['rmssd'], name="HRV",
                            line=dict(color='#3498db', width=2)))
    
    fig.update_layout(title="Training Load vs HRV Trend", xaxis_title="Date",
                      yaxis_title="Value", template='plotly_white', height=400)
    return fig

def create_weekly_hr_metrics(df, session_type="Training"):
    df_filtered = df[df['session_type'] == session_type]
    if df_filtered.empty:
        return go.Figure().update_layout(title=f"No {session_type} Data")
        
    wk = df_filtered.groupby("week")[["max_hr", "avg_hr", "min_hr"]].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wk['week'], y=wk['max_hr'], name="Weekly Max", line=dict(color='#1abc9c')))
    fig.add_trace(go.Scatter(x=wk['week'], y=wk['avg_hr'], name="Weekly Avg", line=dict(color='#3498db')))
    fig.add_trace(go.Scatter(x=wk['week'], y=wk['min_hr'], name="Weekly Min", line=dict(color='#2ecc71')))
    
    fig.update_layout(title=f"HR Metrics on {session_type} sessions", xaxis_title="Week",
                      yaxis_title="BPM", template='plotly_white', height=400)
    return fig

def create_weekly_zone_split(df):
    # Summing minutes in zones 2-5
    wk = df.groupby("week")[[f"zone_{i}_d" for i in range(2, 6)]].sum().reset_index()
    for i in range(2, 6):
        wk[f"zone_{i}_d"] = wk[f"zone_{i}_d"] / 60000 # to min
        
    fig = go.Figure()
    colors = ['#3498db', '#27ae60', '#f1c40f', '#e74c3c']
    for i, color in zip(range(2, 6), colors):
        fig.add_trace(go.Bar(x=wk['week'], y=wk[f"zone_{i}_d"], name=f"Zone {i}", marker_color=color))
        
    fig.update_layout(title="HR zone split up for weeks", xaxis_title="Week Start",
                      yaxis_title="Minutes", barmode='group', template='plotly_white', height=400)
    return fig

def create_avg_training_load_line(df):
    wk = df.groupby("week")["training_load"].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wk['week'], y=wk['training_load'], mode='lines+markers', 
                            line=dict(color='#1abc9c', width=2)))
    fig.update_layout(title="Avg Training load - Line Graph", xaxis_title="Week Start Date",
                      yaxis_title="Load", template='plotly_white', height=350)
    return fig

def create_weekly_acwr_line(df):
    wk = df.groupby("week")["acwr"].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wk['week'], y=wk['acwr'], mode='lines+markers', 
                            line=dict(color='#9b59b6', width=2)))
    fig.update_layout(title="Weekly Avg ACWR - Line Graph", xaxis_title="Week Start Date",
                      yaxis_title="ACWR", template='plotly_white', height=350)
    return fig

def create_session_time_hrv_load(df, time_label="Morning"):
    # Heuristic: Morning is < 12h, Afternoon/Evening is >= 12h
    if time_label == "Morning":
        df_filtered = df[df['session_hour'] < 12]
    else:
        df_filtered = df[df['session_hour'] >= 12]
        
    if df_filtered.empty:
        return go.Figure().update_layout(title=f"No {time_label} Data")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_filtered['session_date'], y=df_filtered['training_load'], 
                         name="training_load", marker_color='#e67e22', opacity=0.6))
    fig.add_trace(go.Scatter(x=df_filtered['session_date'], y=df_filtered['rmssd'], 
                            name="hrv", line=dict(color='#3498db', width=1.5)))
    
    fig.update_layout(title=f"{time_label} session Training and HRV Data", 
                      xaxis_title="session_date", template='plotly_white', height=400)
    return fig

def create_session_quality_graph(df):
    fig = go.Figure()
    
    train = df[df['session_type'] == "Training"]
    ready = df[df['session_type'] == "Readiness"]
    
    fig.add_trace(go.Bar(x=train['session_date'], y=train['session_quality'], 
                         name="Training Sessions", marker_color='#e74c3c', opacity=0.7))
    fig.add_trace(go.Bar(x=ready['session_date'], y=ready['session_quality'], 
                         name="Readiness Sessions", marker_color='#1abc9c', opacity=0.7))
    
    fig.update_layout(title="Session Quality Graph", xaxis_title="Session Date",
                      yaxis_title="Session Quality", barmode='group', 
                      template='plotly_white', height=400)
    return fig
