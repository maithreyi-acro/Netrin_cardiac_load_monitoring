import dash_bootstrap_components as dbc
from dash import dcc, html

def create_header():
    return dbc.Row([
        dbc.Col([
            html.H1(" Cardiac Load Monitoring Dashboard", 
                   className="text-center mb-3 mt-3",
                   style={'fontWeight': 'bold', 'color': '#2c3e50'}),
        ])
    ])

def create_summary_cards(df=None):
    if df is None or len(df) == 0:
        return dbc.Row([dbc.Col(html.P("No data available for this athlete.", className="text-center"))])
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Sessions", className="text-muted"),
                    html.H3(f"{len(df)}", className="text-primary mb-0")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Avg RMSSD", className="text-muted"),
                    html.H3(f"{df['rmssd'].mean():.1f} ms", className="text-success mb-0")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Avg SDNN", className="text-muted"),
                    html.H3(f"{df['sdnn'].mean():.1f} ms", className="text-info mb-0")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Avg Load", className="text-muted"),
                    html.H3(f"{df['training_load'].mean():.1f}", className="text-warning mb-0")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Avg ACWR", className="text-muted"),
                    html.H3(f"{df['acwr'].mean():.2f}", className="text-danger mb-0")
                ])
            ])
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Avg VO₂ Max", className="text-muted"),
                    html.H3(f"{df['vo2_max'].mean():.1f}", className="text-secondary mb-0")
                ])
            ])
        ], width=2),
    ], className="mb-4")

def create_controls(athletes):
    return dbc.Row([
        dbc.Col([
            html.Label("Select Athlete:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='athlete-select',
                options=[{'label': a, 'value': a} for a in athletes],
                value=athletes[0] if athletes else None,
                clearable=False,
                className="mb-3"
            )
        ], width=3),
        dbc.Col([
            html.Label("Time Range:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='date-range',
                options=[
                    {'label': 'Last 7 Days', 'value': 7},
                    {'label': 'Last 14 Days', 'value': 14},
                    {'label': 'Last 30 Days', 'value': 30},
                    {'label': 'Last 60 Days', 'value': 60},
                    {'label': 'Last 90 Days', 'value': 90},
                    {'label': 'All Data', 'value': 999999}
                ],
                value=30,
                clearable=False,
                className="mb-3"
            )
        ], width=3)
    ])

def create_tabs():
    return dbc.Tabs([
        # HRV Tab
        dbc.Tab(label=" HRV Metrics", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id='hrv-rmssd')], width=6),
                dbc.Col([dcc.Graph(id='hrv-sdnn')], width=6),
            ], className="mt-3"),
            dbc.Row([
                dbc.Col([dcc.Graph(id='hrv-pnn50')], width=12),
            ])
        ]),
        
        # Training Load Tab
        dbc.Tab(label=" Training Load", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id='training-load')], width=8),
                dbc.Col([dcc.Graph(id='load-intensity')], width=4),
            ], className="mt-3"),
            dbc.Row([
                dbc.Col([dcc.Graph(id='acwr-trend')], width=8),
                dbc.Col([dcc.Graph(id='acute-chronic')], width=4),
            ])
        ]),
        
        # Cardiac Tab
        dbc.Tab(label=" Heart Rate", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id='rest-hr')], width=6),
                dbc.Col([dcc.Graph(id='avg-hr')], width=6),
            ], className="mt-3"),
            dbc.Row([
                dbc.Col([dcc.Graph(id='max-hr')], width=6),
                dbc.Col([dcc.Graph(id='min-hr')], width=6),
            ])
        ]),
        
        # Metabolic Tab
        dbc.Tab(label=" Metabolic", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id='epoc-total')], width=6),
                dbc.Col([dcc.Graph(id='epoc-peak')], width=6),
            ], className="mt-3"),
            dbc.Row([
                dbc.Col([dcc.Graph(id='vo2')], width=6),
                dbc.Col([dcc.Graph(id='vo2-max')], width=6),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='energy-exp')], width=12),
            ])
        ]),
        
        # Movement Tab
        dbc.Tab(label=" Movement", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id='movement-load')], width=6),
                dbc.Col([dcc.Graph(id='movement-intensity')], width=6),
            ], className="mt-3")
        ]),
        
        # Zones Tab
        dbc.Tab(label=" HR Zones", children=[
            dbc.Row([
                dbc.Col([dcc.Graph(id='zones-stacked')], width=12),
            ], className="mt-3"),
            dbc.Row([
                dbc.Col([dcc.Graph(id='zones-pie')], width=6),
                dbc.Col([dcc.Graph(id='zones-heatmap')], width=6),
            ])
        ]),
    ])

def create_footer():
    return html.Div([
        html.Hr(),
        html.P("Cardiac Load Monitoring Platform", className="text-center text-muted")
    ])
