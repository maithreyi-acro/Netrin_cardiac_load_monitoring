import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from viz.data.load_data import load_summary
from viz.plots import (
    plot_hrv_daily, plot_hrv_weekly,
    plot_training_load_daily, plot_acwr_weekly,
    plot_resting_hr, plot_avg_max_hr,
    plot_epoc, plot_vo2,
    plot_movement_load, plot_movement_intensity,
    plot_zones_weekly, plot_zones_percentage
)

# Page configuration
st.set_page_config(
    page_title="Cardiac Load Monitoring",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
PROCESSED_DIR = "bin/processed"

def get_athletes():
    """Discover available athletes from summary files."""
    if not os.path.exists(PROCESSED_DIR):
        return []
    files = [f for f in os.listdir(PROCESSED_DIR) if f.startswith('hr_summary_') and f.endswith('.csv')]
    return [f.replace('hr_summary_', '').replace('.csv', '') for f in files]

# Sidebar for athlete selection
st.sidebar.title("Athlete")
athletes = get_athletes()

if not athletes:
    # Fallback to legacy
    if os.path.exists(os.path.join(PROCESSED_DIR, "hr_summary.csv")):
        selected_athlete = st.sidebar.selectbox("Select Athlete", ["hr_summary"])
    else:
        st.error("No processed data found. Please run main.py first.")
        st.stop()
else:
    selected_athlete = st.sidebar.selectbox("Select Athlete", athletes)

# Load data
csv_name = f"hr_summary_{selected_athlete}.csv" if selected_athlete != "hr_summary" else "hr_summary.csv"
DATA_PATH = os.path.join(PROCESSED_DIR, csv_name)

@st.cache_data
def load_data(path):
    return load_summary(path)

df = load_data(DATA_PATH)

# Header
st.title(" Cardiac Load Monitoring Dashboard")
st.caption("Seaborn/Matplotlib Visualization")
st.markdown("---")

# Summary metrics
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Sessions", f"{len(df)}")
with col2:
    st.metric("Avg RMSSD", f"{df['rmssd'].mean():.1f} ms")
with col3:
    st.metric("Avg SDNN", f"{df['sdnn'].mean():.1f} ms")
with col4:
    st.metric("Avg Load", f"{df['training_load'].mean():.1f}")
with col5:
    st.metric("Avg ACWR", f"{df['acwr'].mean():.2f}")
with col6:
    st.metric("Avg VO₂ Max", f"{df['vo2_max'].mean():.1f}")

st.markdown("---")

# Sidebar for filtering
st.sidebar.title(" Filters")
days = st.sidebar.selectbox(
    "Time Range",
    options=[7, 14, 30, 60, 90, len(df)],
    format_func=lambda x: f"Last {x} Days" if x < len(df) else "All Data",
    index=2
)

df_filtered = df.tail(days)

# Sidebar navigation
page = st.sidebar.radio(
    "Select Metric Category",
    ["HRV Metrics", "Training Load", "Cardiac Metrics", "Metabolic", "Movement", "HR Zones"]
)

# Main content
if page == "HRV Metrics":
    st.header(" Heart Rate Variability Metrics")
    
    st.subheader("Daily HRV Trends")
    fig = plot_hrv_daily(df_filtered)
    st.pyplot(fig)
    
    st.subheader("Weekly Average HRV")
    fig = plot_hrv_weekly(df_filtered)
    st.pyplot(fig)

elif page == "Training Load":
    st.header(" Training Load & ACWR")
    
    st.subheader("Daily Training Load & Intensity")
    fig = plot_training_load_daily(df_filtered)
    st.pyplot(fig)
    
    st.subheader("Weekly ACWR")
    fig = plot_acwr_weekly(df_filtered)
    st.pyplot(fig)
    
    st.info(" **Optimal ACWR**: 0.8 - 1.5 |  **High Risk**: >1.5 |  **Low Risk**: <0.8")

elif page == "Cardiac Metrics":
    st.header(" Cardiac Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resting HR Trend")
        fig = plot_resting_hr(df_filtered)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average vs Max HR")
        fig = plot_avg_max_hr(df_filtered)
        st.pyplot(fig)

elif page == "Metabolic":
    st.header(" Metabolic Metrics")
    
    st.subheader("EPOC Trends")
    fig = plot_epoc(df_filtered)
    st.pyplot(fig)
    
    st.subheader("VO₂ Metrics")
    fig = plot_vo2(df_filtered)
    st.pyplot(fig)

elif page == "Movement":
    st.header(" Movement Load")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Movement Load")
        fig = plot_movement_load(df_filtered)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Movement Intensity")
        fig = plot_movement_intensity(df_filtered)
        st.pyplot(fig)

elif page == "HR Zones":
    st.header(" Heart Rate Zones")
    
    st.subheader("Weekly Zone Distribution")
    fig = plot_zones_weekly(df_filtered)
    st.pyplot(fig)
    
    st.subheader("Latest Session Zones")
    fig = plot_zones_percentage(df_filtered)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6b7280;'>Cardiac Load Monitoring Platform | Seaborn Visualizations</p>",
    unsafe_allow_html=True
)
