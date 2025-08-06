#!/bin/sh

# Start Flask app
python scripts/dashboard.py &

# Start Dash app
python scripts/prediction.py &

# Start Prometheus exporter
python scripts/prometheus.py &

# Wait for all background processes
wait
