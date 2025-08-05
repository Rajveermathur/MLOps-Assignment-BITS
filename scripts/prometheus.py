import json
from prometheus_client import Gauge, generate_latest
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define Prometheus metrics
total_requests = Gauge('total_requests', 'Total number of requests')
successful_requests = Gauge('successful_requests', 'Number of successful requests')
failed_requests = Gauge('failed_requests', 'Number of failed requests')
average_response_time = Gauge('average_response_time_seconds', 'Average response time in seconds')

def load_metrics():
    try:
        with open("logs/metrics.json", "r") as f:
            data = json.load(f)
            total_requests.set(data.get("total_requests", 0))
            successful_requests.set(data.get("successful_requests", 0))
            failed_requests.set(data.get("failed_requests", 0))
            average_response_time.set(data.get("average_response_time", 0.0))
    except Exception as e:
        print(f"Error loading metrics: {e}")

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            load_metrics()
            self.send_response(200)
            self.send_header("Content-type", "text/plain; version=0.0.4")
            self.end_headers()
            self.wfile.write(generate_latest())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=MetricsHandler):
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting exporter on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
