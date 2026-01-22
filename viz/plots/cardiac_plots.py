import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

# ============ PLOTLY PLOTS  ============
def create_resting_hr_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['rest_hr'],
        mode='markers', marker=dict(size=6, color='#16a085'),
        hovertemplate='<b>%{x}</b><br>Rest HR: %{y:.0f} bpm<extra></extra>'
    ))
    df_temp = df_filtered.copy()
    df_temp['rest_hr_ma'] = df_temp['rest_hr'].rolling(window=7, min_periods=1).mean()
    fig.add_trace(go.Scatter(
        x=df_temp['session_date'], y=df_temp['rest_hr_ma'],
        mode='lines', name='7-Day MA', line=dict(color='#c0392b', width=3)
    ))
    fig.update_layout(title="Resting HR", xaxis_title="Date", yaxis_title="bpm",
                      template='plotly_white', height=350)
    return fig

def create_avg_hr_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['avg_hr'],
        mode='lines+markers', line=dict(color='#3498db', width=2),
        hovertemplate='<b>%{x}</b><br>Avg HR: %{y:.0f} bpm<extra></extra>'
    ))
    fig.update_layout(title="Average HR", xaxis_title="Date", yaxis_title="bpm",
                      template='plotly_white', height=350)
    return fig

def create_max_hr_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['max_hr'],
        mode='lines+markers', line=dict(color='#e74c3c', width=2),
        hovertemplate='<b>%{x}</b><br>Max HR: %{y:.0f} bpm<extra></extra>'
    ))
    fig.update_layout(title="Maximum HR", xaxis_title="Date", yaxis_title="bpm",
                      template='plotly_white', height=350)
    return fig

def create_min_hr_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['min_hr'],
        mode='lines+markers', line=dict(color='#95a5a6', width=2),
        hovertemplate='<b>%{x}</b><br>Min HR: %{y:.0f} bpm<extra></extra>'
    ))
    fig.update_layout(title="Minimum HR", xaxis_title="Date", yaxis_title="bpm",
                      template='plotly_white', height=350)
    return fig

# ============ SEABORN PLOTS  ============
def plot_resting_hr(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(df["session_date"], df["rest_hr"], alpha=0.5, s=50, color='#06A77D', label='Resting HR')
    
    df_temp = df.copy()
    df_temp['rest_hr_ma'] = df_temp['rest_hr'].rolling(window=7, min_periods=1).mean()
    ax.plot(df_temp["session_date"], df_temp["rest_hr_ma"], linewidth=3, 
            color='#E63946', label='7-Day Moving Average')
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("HR (bpm)", fontsize=12)
    ax.set_title("Resting Heart Rate Trend", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_avg_max_hr(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df["session_date"], df["avg_hr"], marker='o', linewidth=2, 
            color='#457B9D', label='Average HR', markersize=5)
    ax.plot(df["session_date"], df["max_hr"], marker='s', linewidth=2, 
            color='#E63946', label='Max HR', markersize=5)
    ax.fill_between(df["session_date"], df["avg_hr"], alpha=0.2, color='#457B9D')
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("HR (bpm)", fontsize=12)
    ax.set_title("Average vs Maximum Heart Rate", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig
