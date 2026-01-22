import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

sns.set_theme(style="whitegrid", context="talk", palette="husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

# ============ PLOTLY PLOTS (for Dashboard) ============

def create_hrv_rmssd_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['rmssd'],
        mode='lines+markers', name='RMSSD', line=dict(color='#3498db', width=2),
        hovertemplate='<b>%{x}</b><br>RMSSD: %{y:.1f} ms<extra></extra>'
    ))
    fig.add_hline(y=df_filtered['rmssd'].mean(), line_dash="dash", line_color="gray")
    fig.update_layout(title="RMSSD Trend", xaxis_title="Date", yaxis_title="ms", 
                      template='plotly_white', height=350)
    return fig

def create_hrv_sdnn_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['sdnn'],
        mode='lines+markers', name='SDNN', line=dict(color='#9b59b6', width=2),
        hovertemplate='<b>%{x}</b><br>SDNN: %{y:.1f} ms<extra></extra>'
    ))
    fig.add_hline(y=df_filtered['sdnn'].mean(), line_dash="dash", line_color="gray")
    fig.update_layout(title="SDNN Trend", xaxis_title="Date", yaxis_title="ms", 
                      template='plotly_white', height=350)
    return fig

def create_hrv_pnn50_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['pnn50'],
        mode='lines+markers', name='pNN50', line=dict(color='#e67e22', width=2),
        fill='tozeroy', hovertemplate='<b>%{x}</b><br>pNN50: %{y:.1f}%<extra></extra>'
    ))
    fig.update_layout(title="pNN50 Trend", xaxis_title="Date", yaxis_title="%", 
                      template='plotly_white', height=350)
    return fig

# ============ SEABORN PLOTS (for Export/Reports) ============

def plot_hrv_daily(df):
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    ax1 = axes[0]
    ax1.plot(df["session_date"], df["rmssd"], marker='o', linewidth=2, label="RMSSD", color='#2E86AB')
    ax1.plot(df["session_date"], df["sdnn"], marker='s', linewidth=2, label="SDNN", color='#A23B72')
    ax1.set_ylabel("ms", fontsize=12)
    ax1.set_title("RMSSD & SDNN Trends", fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    ax2 = axes[1]
    ax2.fill_between(df["session_date"], df["pnn50"], alpha=0.4, color='#F18F01')
    ax2.plot(df["session_date"], df["pnn50"], marker='o', linewidth=2, color='#F18F01', label="pNN50")
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("%", fontsize=12)
    ax2.set_title("pNN50 Trend", fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    return fig

def plot_hrv_weekly(df):
    wk = df.groupby("week")[["rmssd","sdnn"]].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(wk))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], wk["rmssd"], width, label='RMSSD', color='#2E86AB', alpha=0.8)
    ax.bar([i + width/2 for i in x], wk["sdnn"], width, label='SDNN', color='#A23B72', alpha=0.8)
    
    ax.set_xlabel("Week", fontsize=12)
    ax.set_ylabel("ms", fontsize=12)
    ax.set_title("Weekly Average HRV (RMSSD & SDNN)", fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([w.strftime('%Y-%m-%d') for w in wk["week"]], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig
