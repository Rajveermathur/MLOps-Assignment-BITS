#!/bin/sh

mlflow ui --host 0.0.0.0 --port 5001 &

# Start Flask app
python scripts/dashboard.py &

# Start Dash app
python scripts/prediction.py &

# Start Prometheus exporter
python scripts/prometheus.py &

# Wait for all background processes
wait
