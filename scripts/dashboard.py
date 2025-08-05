import dash
import json
from dash import dcc, html
import plotly.graph_objs as go
from datetime import datetime

METRICS_FILE = 'logs/metrics.json'
with open(METRICS_FILE, 'r') as f:
    metrics = json.load(f)

# Derived metrics
success_rate = (metrics["successful_requests"] / metrics["total_requests"]) * 100
failure_rate = (metrics["failed_requests"] / metrics["total_requests"]) * 100
avg_response_time_ms = round(metrics["average_response_time"] * 1000, 2)  # ms
last_request_time = datetime.fromisoformat(metrics["last_request_timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "API Metrics Dashboard"

# Layout
app.layout = html.Div(children=[
    html.H1("API Metrics Dashboard", style={'textAlign': 'center'}),
    html.H4(f"Last Request: {last_request_time}", style={'textAlign': 'center', 'color': 'gray'}),

    # KPIs
    html.Div([
        html.Div([
            html.H3("Total Requests"),
            html.P(metrics["total_requests"])
        ], style={'padding': 20, 'border': '1px solid #ccc', 'borderRadius': 10, 'width': '30%'}),
        
        html.Div([
            html.H3("Success Rate"),
            html.P(f"{success_rate:.2f}%")
        ], style={'padding': 20, 'border': '1px solid #ccc', 'borderRadius': 10, 'width': '30%'}),

        html.Div([
            html.H3("Avg Response Time"),
            html.P(f"{avg_response_time_ms} ms")
        ], style={'padding': 20, 'border': '1px solid #ccc', 'borderRadius': 10, 'width': '30%'})
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': 50}),

    # Pie Chart
    dcc.Graph(
        figure=go.Figure(data=[
            go.Pie(labels=['Successful', 'Failed'],
                   values=[metrics['successful_requests'], metrics['failed_requests']],
                   hole=0.4)
        ]).update_layout(title="Success vs Failure")
    ),

    # Bar Chart
    dcc.Graph(
        figure=go.Figure(data=[
            go.Bar(x=['Total Requests', 'Successful', 'Failed'],
                   y=[metrics['total_requests'], metrics['successful_requests'], metrics['failed_requests']],
                   text=[metrics['total_requests'], metrics['successful_requests'], metrics['failed_requests']],
                   textposition='auto')
        ]).update_layout(title="Request Counts", yaxis_title="Count")
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
