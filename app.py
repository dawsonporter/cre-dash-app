import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Your existing data
commercialRealEstateData = {
    "Multifamily": {
        "Vacancy Rate (%)": [6.4, 6.2, 6.3, 6.5, 6.7, 6.8, 6.7, 6.7, 6.1, 5.3, 4.8, 5.0, 5.1, 5.4, 5.9, 6.5, 6.8, 7.0, 7.3, 7.7, 7.8],
        "Effective Rent Growth (% YoY)": [3.1, 3.0, 3.2, 3.4, 2.8, 1.0, 0.1, 0.4, 2.0, 7.1, 10.5, 11.1, 11.2, 8.9, 5.4, 3.7, 2.6, 1.1, 0.6, 0.7, 0.7],
        "Net Absorption (K Units)": [93.1, 127.9, 78.2, 41.4, 76.5, 89.8, 134.0, 98.9, 190.9, 267.5, 182.9, 60.8, 70.5, 65.0, 21.6, -6.4, 68.4, 97.3, 87.1, 67.1, 109.2],
        "Net Completions (K Units)": [79.7, 101.6, 90.5, 98.4, 116.9, 113.2, 124.0, 100.5, 91.4, 116.6, 106.5, 101.8, 102.1, 109.4, 136.7, 103.9, 129.0, 157.2, 155.9, 143.0, 152.6],
        "Cap Rate (%)": [5.5, 5.4, 5.4, 5.3, 5.2, 5.1, 5.0, 5.0, 5.0, 5.0, 4.8, 4.7, 4.7, 4.7, 4.7, 4.9, 5.2, 5.3, 5.3, 5.5, 5.7],
        "Property Price Index (% QoQ)": [0.6, 2.8, 2.9, 2.1, 2.4, 0.5, 1.4, 2.5, 2.9, 4.8, 6.3, 6.4, 4.1, 3.4, -0.8, -6.2, -4.6, -1.7, -1.7, -2.5, -2.8]
    },
    "Industrial": {
        "Vacancy Rate (%)": [4.7, 4.9, 4.9, 5.0, 5.2, 5.4, 5.5, 5.4, 5.2, 5.0, 4.4, 4.1, 4.0, 3.8, 3.9, 3.9, 4.3, 4.6, 5.2, 5.7, 6.2],
        "Asking Rent Growth (% YoY)": [5.9, 5.8, 5.9, 5.8, 5.8, 5.7, 5.7, 6.0, 6.5, 7.4, 8.3, 9.2, 10.1, 10.7, 10.7, 10.4, 9.8, 9.0, 8.2, 7.2, 5.6],
        "Net Absorption (M Sq. Ft.)": [32.2, 45.8, 52.9, 43.3, 45.9, 39.8, 50.5, 84.8, 90.4, 117.7, 178.2, 134.2, 99.6, 109.5, 91.1, 118.0, 51.1, 42.2, 42.3, 33.9, 15.7],
        "Net Completions (M Sq. Ft.)": [46.8, 69.3, 64.4, 71.3, 77.3, 70.6, 76.2, 82.5, 58.9, 75.7, 86.9, 79.1, 83.3, 75.7, 109.2, 130.5, 119.2, 116.1, 147.5, 146.0, 103.6],
        "Cap Rate (%)": [6.4, 6.4, 6.1, 6.0, 6.3, 6.1, 6.0, 5.9, 5.8, 5.8, 5.5, 5.4, 5.4, 5.3, 5.5, 5.5, 5.8, 6.1, 5.9, 6.3, 6.6],
        "Property Price Index (% QoQ)": [3.1, 2.3, 1.6, 1.7, 1.8, 1.8, 2.7, 3.0, 3.6, 5.0, 6.3, 5.5, 3.4, 2.0, 0.5, -0.3, -0.9, -0.2, 1.4, 2.3, 2.2]
    },
    "Office": {
        "Vacancy Rate (%)": [9.4, 9.3, 9.3, 9.4, 9.4, 9.7, 10.2, 10.7, 11.4, 11.8, 11.8, 11.8, 11.9, 12.0, 12.2, 12.3, 12.7, 13.0, 13.3, 13.5, 13.7],
        "Asking Rent Growth (% YoY)": [3.5, 3.8, 3.9, 4.0, 3.3, 1.7, -0.5, -1.6, -2.2, -1.4, 0.1, 0.6, 1.2, 1.2, 1.2, 1.1, 0.9, 0.8, 0.7, 0.8, 0.8],
        "Net Absorption (M Sq. Ft.)": [8.3, 19.0, 10.8, 12.4, 5.1, -8.4, -33.3, -33.5, -43.6, -15.1, 6.1, 11.2, 1.7, -3.1, -3.1, -1.5, -22.0, -15.8, -15.4, -5.7, -19.4],
        "Net Completions (M Sq. Ft.)": [13.0, 13.1, 15.0, 20.4, 11.1, 9.6, 14.6, 12.5, 12.8, 18.0, 12.4, 10.7, 8.1, 10.7, 8.7, 15.9, 8.2, 13.3, 9.6, 9.3, 4.4],
        "Cap Rate (%)": [6.6, 6.7, 6.5, 6.5, 6.5, 6.5, 6.6, 6.6, 6.6, 6.5, 6.2, 6.1, 6.1, 6.3, 6.2, 6.8, 6.7, 6.8, 7.2, 7.2, 7.3],
        "Property Price Index (% QoQ)": [0.3, 1.2, 1.5, 0.7, -0.2, -1.1, 0.7, 2.3, 2.0, 3.7, 4.0, 1.9, 0.9, 0.5, -1.4, -3.4, -4.0, -4.3, -4.9, -5.0, -3.6]
    },
    "Retail": {
        "Vacancy Rate (%)": [4.4, 4.4, 4.4, 4.5, 4.6, 4.7, 4.9, 5.1, 5.0, 5.0, 4.7, 4.6, 4.5, 4.3, 4.3, 4.2, 4.2, 4.1, 4.1, 4.1, 4.1],
        "Asking Rent Growth (% YoY)": [2.5, 2.4, 2.6, 2.6, 2.5, 2.4, 2.0, 1.9, 2.0, 2.5, 3.0, 3.6, 4.0, 4.3, 4.3, 4.3, 4.1, 4.0, 3.9, 3.6, 3.1],
        "Net Absorption (M Sq. Ft.)": [7.0, 13.3, 11.0, 10.0, -1.5, -9.5, -15.5, -2.1, 4.9, 14.9, 31.1, 22.1, 19.5, 21.6, 13.1, 22.0, 9.9, 13.3, 13.1, 16.2, 3.9],
        "Net Completions (M Sq. Ft.)": [13.0, 13.2, 14.6, 17.2, 11.5, 7.8, 12.0, 13.7, 4.3, 7.8, 2.8, 4.5, 3.4, 5.0, 8.0, 7.7, 10.3, 11.4, 10.2, 9.8, 9.9],
        "Cap Rate (%)": [6.5, 6.6, 6.6, 6.6, 6.5, 6.5, 6.6, 6.5, 6.5, 6.6, 6.4, 6.4, 6.3, 6.2, 6.2, 6.6, 6.6, 6.8, 6.6, 7.0, 7.3],
        "Property Price Index (% QoQ)": [0.3, 0.6, 0.4, -0.1, -1.0, -1.5, -0.6, 0.8, 2.6, 3.7, 5.2, 4.6, 2.5, 2.5, -0.4, -3.0, -3.4, -1.4, 0.0, 0.0, 0.2]
    },
    "Hotel": {
        "Occupancy Rate (%)": [61.4, 69.7, 70.5, 61.4, 51.9, 33.2, 47.9, 41.6, 46.0, 60.9, 64.6, 57.8, 56.0, 66.7, 67.4, 59.8, 59.4, 66.3, 67.1, 58.9, 58.2],
        "Average Daily Rate (% YoY)": [1.2, 1.3, 0.8, 1.0, -4.5, -38.7, -24.4, -27.7, -20.0, 45.9, 36.9, 42.8, 38.4, 27.7, 12.5, 12.5, 10.9, 3.3, 2.3, 3.0, 2.3],
        "Revenue Per Available Room (% YoY)": [1.2, 0.9, 0.5, 0.5, -18.4, -70.2, -48.7, -51.0, -29.5, 163.2, 85.1, 97.5, 68.5, 39.3, 17.1, 16.8, 17.0, 2.7, 1.8, 1.4, 0.2]
    }
}

years = [2019, 2020, 2021, 2022, 2023, 2024]
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

def format_data(data):
    formatted_data = []
    for i, values in enumerate(zip(*data.values())):
        year = years[i // 4]
        quarter = quarters[i % 4]
        entry = {'name': f"{year} {quarter}"}
        entry.update({metric: value for metric, value in zip(data.keys(), values)})
        formatted_data.append(entry)
    return pd.DataFrame(formatted_data)

def calculate_correlation(x, y):
    return np.corrcoef(x, y)[0, 1]

def get_correlation_color(corr):
    if corr > 0.7:
        return '#38a169'
    elif corr > 0.4:
        return '#38b2ac'
    elif corr > 0:
        return '#4299e1'
    elif corr > -0.4:
        return '#ed8936'
    elif corr > -0.7:
        return '#e53e3e'
    else:
        return '#9b2c2c'

def get_correlation_description(corr):
    if corr > 0.7:
        return 'Strong Positive'
    elif corr > 0.4:
        return 'Moderate Positive'
    elif corr > 0:
        return 'Weak Positive'
    elif corr > -0.4:
        return 'Weak Negative'
    elif corr > -0.7:
        return 'Moderate Negative'
    else:
        return 'Strong Negative'

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Commercial Real Estate Dashboard", 
            style={'textAlign': 'center', 'color': '#2d3748', 'marginBottom': '20px'}),
    
    html.Div([
        html.Div([
            html.Label("Property Type", style={'color': '#4a5568', 'fontSize': '0.9rem'}),
            dcc.Dropdown(
                id='property-type-dropdown',
                options=[{'label': k, 'value': k} for k in commercialRealEstateData.keys()],
                value='Multifamily',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Primary Metric", style={'color': '#4a5568', 'fontSize': '0.9rem'}),
            dcc.Dropdown(
                id='primary-metric-dropdown',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '5%'}),
        
        html.Div([
            html.Label("Secondary Metric", style={'color': '#4a5568', 'fontSize': '0.9rem'}),
            dcc.Dropdown(
                id='secondary-metric-dropdown',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '5%'})
    ], style={'marginBottom': '20px'}),
    
    dcc.Graph(id='metrics-chart'),
    
    html.Div(id='correlation-indicator', style={'textAlign': 'center', 'marginTop': '20px'}),

    html.Div(
        "Source: MSCI Real Capital Analytics, CoStar Inc. and Wells Fargo Economics",
        style={
            'textAlign': 'center',
            'color': '#718096',
            'fontSize': '0.8rem',
            'marginTop': '30px',
            'borderTop': '1px solid #e2e8f0',
            'paddingTop': '10px'
        }
    )
], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1000px', 'margin': '0 auto', 'padding': '20px', 'backgroundColor': '#f8fafc', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'})

@app.callback(
    [Output('primary-metric-dropdown', 'options'),
     Output('secondary-metric-dropdown', 'options'),
     Output('primary-metric-dropdown', 'value'),
     Output('secondary-metric-dropdown', 'value')],
    [Input('property-type-dropdown', 'value')]
)
def update_metric_dropdowns(selected_property_type):
    options = [{'label': k, 'value': k} for k in commercialRealEstateData[selected_property_type].keys()]
    return options, options, options[0]['value'], options[1]['value']

@app.callback(
    [Output('metrics-chart', 'figure'),
     Output('correlation-indicator', 'children')],
    [Input('property-type-dropdown', 'value'),
     Input('primary-metric-dropdown', 'value'),
     Input('secondary-metric-dropdown', 'value')]
)
def update_chart(property_type, primary_metric, secondary_metric):
    df = format_data(commercialRealEstateData[property_type])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['name'],
        y=df[primary_metric],
        name=primary_metric,
        line=dict(color="#4299e1")
    ))
    
    fig.add_trace(go.Scatter(
        x=df['name'],
        y=df[secondary_metric],
        name=secondary_metric,
        line=dict(color="#38a169"),
        yaxis="y2"
    ))
    
    fig.update_layout(
        title="Commercial Real Estate Metrics Comparison",
        xaxis_title=None,
        yaxis_title=primary_metric,
        yaxis2=dict(title=secondary_metric, overlaying='y', side='right'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    correlation = calculate_correlation(df[primary_metric], df[secondary_metric])
    corr_color = get_correlation_color(correlation)
    corr_description = get_correlation_description(correlation)
    
    correlation_indicator = html.Div([
        html.H3("Correlation"),
        html.Div(
            f"{corr_description}: {correlation:.2f}",
            style={
                'display': 'inline-block',
                'padding': '8px 15px',
                'backgroundColor': corr_color,
                'color': 'white',
                'borderRadius': '20px',
                'fontWeight': 'bold'
            }
        )
    ])
    
    return fig, correlation_indicator

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False, host='0.0.0.0', port=port)
