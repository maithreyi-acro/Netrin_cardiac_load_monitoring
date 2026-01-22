import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ============ PLOTLY PLOTS (for Dashboard) ============

def create_epoc_total_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['epoc_total'],
        mode='lines+markers', line=dict(color='#9b59b6', width=2),
        fill='tozeroy', hovertemplate='<b>%{x}</b><br>EPOC Total: %{y:.2f}<extra></extra>'
    ))
    fig.update_layout(title="EPOC Total", xaxis_title="Date", yaxis_title="EPOC",
                      template='plotly_white', height=350)
    return fig

def create_epoc_peak_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['epoc_peak'],
        mode='lines+markers', line=dict(color='#e67e22', width=2),
        hovertemplate='<b>%{x}</b><br>EPOC Peak: %{y:.2f}<extra></extra>'
    ))
    fig.update_layout(title="EPOC Peak", xaxis_title="Date", yaxis_title="EPOC",
                      template='plotly_white', height=350)
    return fig

def create_vo2_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['vo2'],
        mode='lines+markers', line=dict(color='#27ae60', width=2),
        hovertemplate='<b>%{x}</b><br>VO₂: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="VO₂", xaxis_title="Date", yaxis_title="ml/kg/min",
                      template='plotly_white', height=350)
    return fig

def create_vo2max_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['vo2_max'],
        mode='lines+markers', line=dict(color='#2980b9', width=2),
        hovertemplate='<b>%{x}</b><br>VO₂ Max: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="VO₂ Max", xaxis_title="Date", yaxis_title="ml/kg/min",
                      template='plotly_white', height=350)
    return fig

def create_energy_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtered['session_date'], y=df_filtered['ee_men'],
        marker_color='#d35400', hovertemplate='<b>%{x}</b><br>Energy: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="Energy Expenditure", xaxis_title="Date", yaxis_title="kcal/min",
                      template='plotly_white', height=350)
    return fig

# ============ SEABORN PLOTS (for Export/Reports) ============

def plot_epoc(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1 = axes[0]
    ax1.plot(df["session_date"], df["epoc_total"], marker='o', linewidth=2, 
             color='#9D4EDD', markersize=5)
    ax1.fill_between(df["session_date"], df["epoc_total"], alpha=0.3, color='#9D4EDD')
    ax1.set_xlabel("Date", fontsize=11)
    ax1.set_ylabel("EPOC Total", fontsize=11)
    ax1.set_title("EPOC Total", fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    ax2 = axes[1]
    ax2.plot(df["session_date"], df["epoc_peak"], marker='s', linewidth=2, 
             color='#F77F00', markersize=5)
    ax2.set_xlabel("Date", fontsize=11)
    ax2.set_ylabel("EPOC Peak", fontsize=11)
    ax2.set_title("EPOC Peak", fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_vo2(df):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df["session_date"], df["vo2"], marker='o', linewidth=2, 
            color='#06A77D', label='VO₂', markersize=5)
    ax.plot(df["session_date"], df["vo2_max"], marker='s', linewidth=2, 
            color='#0077B6', label='VO₂ Max', markersize=5)
    
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("ml/kg/min", fontsize=12)
    ax.set_title("VO₂ Metrics", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig
