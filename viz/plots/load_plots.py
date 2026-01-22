import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ============ PLOTLY PLOTS (for Dashboard) ============

def create_training_load_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtered['session_date'], y=df_filtered['training_load'],
        marker_color='#e74c3c', name='Training Load',
        hovertemplate='<b>%{x}</b><br>Load: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="Training Load (TRIMP)", xaxis_title="Date", yaxis_title="TRIMP",
                      template='plotly_white', height=350)
    return fig

def create_load_intensity_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['training_intensity'],
        mode='lines+markers', line=dict(color='#16a085', width=2),
        hovertemplate='<b>%{x}</b><br>Intensity: %{y:.2f}<extra></extra>'
    ))
    fig.update_layout(title="Training Intensity", xaxis_title="Date", yaxis_title="TRIMP/min",
                      template='plotly_white', height=350)
    return fig

def create_acwr_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['acwr'],
        mode='lines+markers', line=dict(color='#2ecc71', width=3),
        marker=dict(size=8), hovertemplate='<b>%{x}</b><br>ACWR: %{y:.2f}<extra></extra>'
    ))
    fig.add_hrect(y0=0.8, y1=1.5, fillcolor="green", opacity=0.1)
    fig.add_hline(y=1.5, line_dash="dash", line_color="red")
    fig.add_hline(y=0.8, line_dash="dash", line_color="orange")
    fig.update_layout(title="ACWR (Injury Risk)", xaxis_title="Date", yaxis_title="ACWR",
                      template='plotly_white', height=350)
    return fig

def create_acute_chronic_plotly(df_filtered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['acute_load'],
        mode='lines', name='Acute', line=dict(color='#e74c3c'),
        hovertemplate='<b>%{x}</b><br>Acute: %{y:.1f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered['session_date'], y=df_filtered['chronic_load'],
        mode='lines', name='Chronic', line=dict(color='#3498db'),
        hovertemplate='<b>%{x}</b><br>Chronic: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(title="Acute vs Chronic Load", xaxis_title="Date", yaxis_title="Load",
                      template='plotly_white', height=350)
    return fig

# ============ SEABORN PLOTS (for Export/Reports) ============

def plot_training_load_daily(df):
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    ax1 = axes[0]
    ax1.bar(df["session_date"], df["training_load"], color='#E63946', alpha=0.7, edgecolor='black')
    ax1.set_ylabel("TRIMP", fontsize=12)
    ax1.set_title("Daily Training Load", fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    ax2 = axes[1]
    ax2.plot(df["session_date"], df["training_intensity"], marker='o', linewidth=2.5, 
             color='#457B9D', markersize=6)
    ax2.fill_between(df["session_date"], df["training_intensity"], alpha=0.3, color='#457B9D')
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("TRIMP/min", fontsize=12)
    ax2.set_title("Training Intensity", fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    return fig

def plot_acwr_weekly(df):
    wk = df.groupby("week")["acwr"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(wk["week"], wk["acwr"], marker='o', linewidth=3, markersize=8, 
            color='#06A77D', label='ACWR')
    ax.axhline(y=1.5, linestyle='--', linewidth=2, color='red', alpha=0.7, label='High Risk (>1.5)')
    ax.axhline(y=0.8, linestyle='--', linewidth=2, color='orange', alpha=0.7, label='Low Risk (<0.8)')
    ax.axhspan(0.8, 1.5, alpha=0.1, color='green', label='Optimal Zone')
    
    ax.set_xlabel("Week", fontsize=12)
    ax.set_ylabel("ACWR", fontsize=12)
    ax.set_title("Weekly Acute:Chronic Workload Ratio (ACWR)", fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig
