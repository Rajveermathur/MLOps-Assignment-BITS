import json
import dash
from dash import dcc, html
import plotly.graph_objs as go
from collections import deque
import datetime

# App setup
app = dash.Dash(__name__)
app.title = "API Metrics Dashboard"

# Simulated historical data store
history_length = 20
timestamps = deque(maxlen=history_length)
avg_response_times = deque(maxlen=history_length)

# Load metrics from JSON file
def load_metrics():
    with open('metrics.json') as f:
        return json.load(f)

# App layout
app.layout = html.Div([
    html.H1("📊 API Metrics Dashboard"),
    
    dcc.Interval(id='interval', interval=5000, n_intervals=0),  # auto-update every 5s

    html.Div(id='stats', style={'display': 'flex', 'justify-content': 'space-around'}),

    html.Br(),

    html.Div([
        dcc.Graph(id='bar_chart'),
        dcc.Graph(id='line_chart')
    ])
])

# Update callback
@app.callback(
    [dash.Output('stats', 'children'),
     dash.Output('bar_chart', 'figure'),
     dash.Output('line_chart', 'figure')],
    [dash.Input('interval', 'n_intervals')]
)
def update_dashboard(n):
    data = load_metrics()

    # Update historical data
    ts = data.get('last_request_timestamp', str(datetime.datetime.now()))
    rt = data.get('average_response_time', 0)
    timestamps.append(ts)
    avg_response_times.append(rt)

    # Stat cards
    stats = [
        html.Div([
            html.H3("Total Requests"),
            html.P(data['total_requests'], style={'fontSize': 24})
        ]),
        html.Div([
            html.H3("Successful Requests"),
            html.P(data['successful_requests'], style={'fontSize': 24})
        ]),
        html.Div([
            html.H3("Failed Requests"),
            html.P(data['failed_requests'], style={'fontSize': 24})
        ]),
        html.Div([
            html.H3("Avg Response Time (s)"),
            html.P(f"{rt:.4f}", style={'fontSize': 24})
        ])
    ]

    # Bar chart
    bar_fig = go.Figure(data=[
        go.Bar(name='Requests', x=['Total', 'Successful', 'Failed'],
               y=[data['total_requests'], data['successful_requests'], data['failed_requests']])
    ])
    bar_fig.update_layout(title="Request Counts", yaxis_title="Count")

    # Line chart for average response time
    line_fig = go.Figure(data=[
        go.Scatter(x=list(timestamps), y=list(avg_response_times), mode='lines+markers')
    ])
    line_fig.update_layout(title="Average Response Time Over Time",
                           xaxis_title="Timestamp", yaxis_title="Response Time (s)")

    return stats, bar_fig, line_fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
