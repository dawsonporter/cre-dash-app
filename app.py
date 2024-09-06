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
        "Vacancy Rate (%)": [6.4, 6.2, 6.3, 6.6, 6.7, 6.8, 6.7, 6.7, 6.1, 5.3, 4.8, 5.0, 5.2, 5.4, 5.9, 6.5, 6.8, 7.0, 7.3, 7.7, 7.8, 7.8],
        "Effective Rent Growth (% YoY)": [3.1, 3.0, 3.2, 3.4, 2.8, 1.0, 0.1, 0.4, 2.0, 7.0, 10.4, 11.0, 11.0, 8.8, 5.4, 3.7, 2.6, 1.1, 0.6, 0.7, 0.7, 0.9],
        "Net Absorption (K Units)": [93.3, 128.0, 78.8, 41.8, 76.8, 90.1, 134.7, 99.5, 190.8, 268.2, 182.8, 61.6, 69.7, 64.5, 21.2, -8.0, 68.8, 98.3, 87.3, 71.3, 117.4, 168.0],
        "Net Completions (K Units)": [79.6, 101.6, 91.6, 99.0, 117.2, 113.7, 125.0, 101.5, 90.4, 116.7, 107.5, 102.7, 101.0, 108.6, 136.5, 104.0, 128.9, 158.7, 157.5, 145.4, 158.3, 186.0],
        "Cap Rate (%)": [5.5, 5.4, 5.4, 5.3, 5.2, 5.1, 5.0, 5.0, 5.0, 5.0, 4.8, 4.7, 4.7, 4.7, 4.7, 4.9, 5.2, 5.3, 5.3, 5.5, 5.7, 5.7],
        "Property Price Index (% QoQ)": [0.5, 2.8, 3.0, 2.1, 2.3, 0.4, 1.3, 2.5, 2.8, 4.9, 6.4, 6.2, 4.1, 3.4, -0.8, -6.0, -4.6, -1.8, -1.5, -2.0, -2.5, -2.4]
    },
    "Industrial": {
        "Vacancy Rate (%)": [4.7, 4.8, 4.9, 5.0, 5.2, 5.3, 5.5, 5.4, 5.2, 5.0, 4.4, 4.1, 4.0, 3.8, 3.9, 3.9, 4.2, 4.6, 5.1, 5.7, 6.2, 6.5],
        "Asking Rent Growth (% YoY)": [5.9, 5.8, 5.8, 5.8, 5.8, 5.7, 5.7, 6.0, 6.5, 7.3, 8.2, 9.1, 9.9, 10.4, 10.4, 10.1, 9.6, 8.9, 8.1, 7.3, 6.0, 4.3],
        "Net Absorption (M Sq. Ft.)": [33.2, 45.8, 53.2, 44.6, 45.7, 39.2, 50.3, 85.5, 90.7, 117.5, 177.9, 135.4, 99.0, 111.3, 91.7, 120.2, 53.6, 45.7, 41.9, 33.6, 10.2, 30.3],
        "Net Completions (M Sq. Ft.)": [47.6, 69.6, 65.5, 72.7, 76.8, 70.3, 75.6, 83.7, 58.8, 74.7, 87.0, 80.9, 83.2, 76.9, 109.2, 131.7, 121.4, 117.3, 146.5, 148.9, 103.4, 102.3],
        "Cap Rate (%)": [6.4, 6.4, 6.1, 6.0, 6.4, 6.2, 6.0, 5.9, 5.9, 5.8, 5.6, 5.4, 5.5, 5.3, 5.5, 5.6, 5.8, 6.0, 5.9, 6.3, 6.5, 6.5],
        "Property Price Index (% QoQ)": [3.1, 2.3, 1.7, 1.7, 1.7, 1.7, 2.6, 2.8, 3.5, 5.0, 6.2, 5.5, 3.2, 1.9, 0.4, -0.4, -0.7, 0.1, 1.5, 2.2, 2.2, 2.5]
    },
    "Office": {
        "Vacancy Rate (%)": [9.3, 9.3, 9.3, 9.4, 9.4, 9.6, 10.2, 10.7, 11.4, 11.8, 11.8, 11.8, 11.9, 12.0, 12.1, 12.3, 12.7, 13.0, 13.3, 13.4, 13.7, 13.8],
        "Asking Rent Growth (% YoY)": [3.6, 3.8, 3.9, 4.0, 3.3, 1.7, -0.5, -1.6, -2.2, -1.4, 0.1, 0.6, 1.3, 1.3, 1.3, 1.1, 0.8, 0.8, 0.7, 0.9, 0.9, 0.8],
        "Net Absorption (M Sq. Ft.)": [8.8, 19.2, 10.5, 12.6, 6.0, -8.2, -35.0, -33.4, -43.3, -16.0, 6.8, 12.0, 1.1, -3.1, -3.9, -0.5, -22.8, -16.4, -16.0, -6.7, -22.4, 2.1],
        "Net Completions (M Sq. Ft.)": [13.4, 13.6, 14.7, 20.3, 12.4, 9.5, 13.0, 12.4, 13.4, 16.8, 12.8, 11.0, 7.9, 10.2, 8.7, 16.3, 8.0, 12.8, 9.3, 6.8, 4.4, 5.6],
        "Cap Rate (%)": [6.6, 6.7, 6.5, 6.5, 6.5, 6.6, 6.6, 6.6, 6.6, 6.5, 6.2, 6.1, 6.1, 6.3, 6.2, 6.8, 6.8, 6.7, 7.1, 7.2, 7.3, 7.1],
        "Property Price Index (% QoQ)": [0.5, 1.3, 1.5, 0.5, -0.5, -1.5, 0.8, 2.6, 1.9, 3.5, 4.1, 1.8, 0.9, 0.6, -1.4, -3.4, -4.0, -4.3, -4.9, -4.8, -3.2, -1.0]
    },
    "Retail": {
        "Vacancy Rate (%)": [4.4, 4.4, 4.4, 4.4, 4.5, 4.7, 4.9, 5.0, 5.0, 5.0, 4.7, 4.6, 4.4, 4.3, 4.3, 4.1, 4.1, 4.1, 4.1, 4.0, 4.1, 4.1],
        "Asking Rent Growth (% YoY)": [2.5, 2.5, 2.6, 2.6, 2.5, 2.5, 2.1, 2.0, 2.1, 2.5, 3.1, 3.6, 4.0, 4.2, 4.3, 4.3, 4.1, 4.0, 3.9, 3.6, 3.3, 2.7],
        "Net Absorption (M Sq. Ft.)": [7.5, 13.3, 11.0, 10.1, -0.8, -9.6, -15.5, -2.3, 5.7, 15.1, 33.0, 22.0, 18.6, 22.3, 12.2, 22.6, 8.7, 12.8, 12.7, 16.5, 4.0, 7.5],
        "Net Completions (M Sq. Ft.)": [13.4, 13.2, 14.7, 17.6, 10.9, 6.9, 13.6, 13.7, 5.0, 7.8, 3.8, 4.8, 3.3, 4.8, 7.5, 7.6, 10.3, 10.7, 10.0, 10.1, 7.0, 7.1],
        "Cap Rate (%)": [6.6, 6.6, 6.6, 6.6, 6.5, 6.5, 6.6, 6.5, 6.5, 6.6, 6.5, 6.4, 6.3, 6.2, 6.2, 6.6, 6.5, 6.7, 6.6, 6.9, 7.1, 7.0],
        "Property Price Index (% QoQ)": [0.4, 0.5, 0.2, -0.1, -0.9, -1.4, -0.6, 0.8, 2.6, 3.7, 5.1, 4.6, 2.6, 2.3, -0.5, -3.0, -3.3, -1.4, -0.2, -0.5, -0.5, 0.1]
    },
    "Hotel": {
        "Occupancy Rate (%)": [61.4, 69.7, 70.5, 61.4, 51.9, 33.2, 47.9, 41.6, 46.0, 60.9, 64.7, 57.8, 56.0, 66.7, 67.4, 59.9, 59.4, 66.3, 67.1, 58.9, 58.3, 66.8],
        "Average Daily Rate (% YoY)": [1.2, 1.3, 0.8, 1.0, -4.5, -38.7, -24.4, -27.7, -20.0, 45.9, 36.9, 42.7, 38.4, 27.7, 12.5, 12.5, 10.8, 3.3, 2.3, 3.0, 2.1, 1.6],
        "Revenue Per Available Room (% YoY)": [1.1, 0.9, 0.5, 0.5, -18.4, -70.2, -48.6, -50.9, -29.5, 163.3, 85.1, 97.5, 68.6, 39.4, 17.1, 16.8, 17.1, 2.7, 1.8, 1.5, 0.1, 2.4]
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
        title=f"CRE Metrics Comparison - {property_type}",
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
