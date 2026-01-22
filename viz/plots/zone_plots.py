import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

ZONE_COLS = [f"zone_{i}_d" for i in range(6)]
ZONE_NAMES = ["Zone 0\n(50-60%)", "Zone 1\n(60-70%)", "Zone 2\n(70-80%)", 
              "Zone 3\n(80-90%)", "Zone 4\n(90-100%)", "Zone 5\n(100%+)"]
ZONE_COLORS = ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51', '#D62828']
ZONE_COLORS_PLOTLY = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#34495e']

# ============ PLOTLY PLOTS (for Dashboard) ============

def create_zones_stacked_plotly(df_filtered):
    wk = df_filtered.groupby("week")[[f"zone_{i}_d" for i in range(6)]].sum().reset_index()
    for col in [f"zone_{i}_d" for i in range(6)]:
        wk[col] = wk[col] / 60000
    
    fig = go.Figure()
    for i in range(6):
        fig.add_trace(go.Bar(
            x=wk['week'], y=wk[f'zone_{i}_d'], name=f'Zone {i}',
            marker_color=ZONE_COLORS_PLOTLY[i], 
            hovertemplate=f'<b>%{{x}}</b><br>Zone {i}: %{{y:.1f}} min<extra></extra>'
        ))
    fig.update_layout(title="Weekly HR Zone Distribution", xaxis_title="Week", 
                      yaxis_title="Time (min)", barmode='stack',
                      template='plotly_white', height=400)
    return fig

def create_zones_pie_plotly(df_filtered):
    latest = df_filtered.iloc[-1]
    zone_pcts = [latest[f"zone_{i}_pct"] for i in range(6)]
    fig = go.Figure(data=[go.Pie(
        labels=[f'Zone {i}' for i in range(6)], values=zone_pcts,
        marker=dict(colors=ZONE_COLORS_PLOTLY), hole=0.4,
        hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
    )])
    fig.update_layout(title="Latest Session Zones", template='plotly_white', height=400)
    return fig

def create_zones_heatmap_plotly(df_filtered):
    zone_data = df_filtered[["session_date"] + [f"zone_{i}_pct" for i in range(6)]].set_index("session_date")
    fig = go.Figure(data=go.Heatmap(
        z=zone_data.T.values, x=zone_data.index, y=[f'Zone {i}' for i in range(6)],
        colorscale='Viridis', hovertemplate='<b>%{x}</b><br>%{y}: %{z:.1f}%<extra></extra>'
    ))
    fig.update_layout(title="Zone Distribution Heatmap", xaxis_title="Date",
                      template='plotly_white', height=400)
    return fig

# ============ SEABORN PLOTS (for Export/Reports) ============

def plot_zones_weekly(df):
    wk = df.groupby("week")[ZONE_COLS].sum().reset_index()
    for col in ZONE_COLS:
        wk[col] = wk[col] / 60000
    
    fig, ax = plt.subplots(figsize=(14, 7))
    bottom = np.zeros(len(wk))
    for i, (col, name, color) in enumerate(zip(ZONE_COLS, ZONE_NAMES, ZONE_COLORS)):
        ax.bar(range(len(wk)), wk[col], bottom=bottom, label=name, 
               color=color, alpha=0.85, edgecolor='white', linewidth=0.5)
        bottom += wk[col]
    
    ax.set_xlabel("Week", fontsize=12)
    ax.set_ylabel("Time (minutes)", fontsize=12)
    ax.set_title("Weekly HR Zone Distribution", fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(wk)))
    ax.set_xticklabels([w.strftime('%Y-%m-%d') for w in wk["week"]], rotation=45, ha='right')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

def plot_zones_percentage(df):
    latest = df.iloc[-1]
    zone_pcts = [latest[f"zone_{i}_pct"] for i in range(6)]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(zone_pcts, labels=ZONE_NAMES, autopct='%1.1f%%',
                                        colors=ZONE_COLORS, startangle=90,
                                        textprops={'fontsize': 11, 'weight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
    
    ax.set_title(f"HR Zone Distribution - Latest Session\n({latest['session']})", 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    return fig
