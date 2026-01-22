import dash
import dash_bootstrap_components as dbc
from dash import html
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from viz.data.load_data import load_summary
from viz.components import (
    create_header, create_summary_cards, create_controls, 
    create_tabs, create_footer, register_callbacks
)

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Cardiac Load Monitoring"

# Configuration
PROCESSED_DIR = "bin/processed"

def get_athletes():
    if not os.path.exists(PROCESSED_DIR):
        return []
    files = [f for f in os.listdir(PROCESSED_DIR) if f.startswith('hr_summary_') and f.endswith('.csv')]
    return [f.replace('hr_summary_', '').replace('.csv', '') for f in files]

athletes = get_athletes()
if not athletes:
    # Check if a legacy hr_summary.csv exists
    if os.path.exists(os.path.join(PROCESSED_DIR, "hr_summary.csv")):
        athletes = ["General"]
    else:
        athletes = []

# Build layout
app.layout = dbc.Container([
    create_header(),
    create_controls(athletes),
    html.Div(id='summary-cards-container'),
    create_tabs(),
    create_footer()
], fluid=True, style={'backgroundColor': '#f8f9fa'})

# Register callbacks
register_callbacks(app, PROCESSED_DIR)

if __name__ == '__main__':
    print(f"Found athletes: {athletes}")
    print("Dashboard running at http://127.0.0.1:8050/")
    app.run(debug=True, port=8050)
