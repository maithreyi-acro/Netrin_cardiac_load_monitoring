import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ============ PLOTLY PLOTS (for Dashboard) ============

def create_movement_load_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtered['session_date'], y=df_filtered['movement_load'],
        marker_color='#16a085', hovertemplate='<b>%{x}</b><br>Load: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="Movement Load", xaxis_title="Date", yaxis_title="Load",
                      template='plotly_white', height=350)
    return fig

def create_movement_intensity_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['movement_load_intensity'],
        mode='lines+markers', line=dict(color='#8e44ad', width=2),
        hovertemplate='<b>%{x}</b><br>Intensity: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="Movement Intensity", xaxis_title="Date", yaxis_title="Intensity",
                      template='plotly_white', height=350)
    return fig

# ============ SEABORN PLOTS (for Export/Reports) ============

def plot_movement_load(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(df["session_date"], df["movement_load"], color='#52B788', alpha=0.7, edgecolor='black')
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Movement Load", fontsize=12)
    ax.set_title("Daily Movement Load", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_movement_intensity(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df["session_date"], df["movement_load_intensity"], marker='o', linewidth=2.5, 
            color='#D946EF', markersize=6)
    ax.fill_between(df["session_date"], df["movement_load_intensity"], alpha=0.3, color='#D946EF')
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Intensity", fontsize=12)
    ax.set_title("Movement Load Intensity", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig
