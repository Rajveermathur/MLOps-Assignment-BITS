from flask import Flask, request, jsonify, g
from pydantic import BaseModel, ValidationError, Field
import pandas as pd
import joblib
import json
import os
from datetime import datetime
import time

LOG_FILE = 'logs/predictions.json'
METRICS_FILE = 'logs/metrics.json'

def init_metrics():
    if not os.path.exists(METRICS_FILE):
        initial_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "last_request_timestamp": None
        }
        with open(METRICS_FILE, 'w') as f:
            json.dump(initial_metrics, f, indent=2)

# Initialize Flask app
app = Flask(__name__)
init_metrics()

# Load the model
# with open('models/California_Housing_model.pkl', 'rb') as f:
    # model = pickle.load(f)
model = joblib.load('models/California_Housing_model.pkl')

# Define input schema
class HousingInput(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

def read_metrics():
    try:
        with open(METRICS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        init_metrics()
        return read_metrics()

def write_metrics(metrics):
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)

def update_average_response_time(old_avg, new_time, count):
    if count == 1:
        return new_time
    return ((old_avg * (count - 1)) + new_time) / count

def append_to_json_log(new_entry):
    try:
        # If file doesn't exist, create it with empty list
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f, indent=2)

        # Read existing data (handle if corrupted)
        try:
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

        # Append new entry
        data.append(new_entry)

        # Write back
        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Error logging prediction: {e}")

@app.route('/')
def home():
    return jsonify({"message": "California Housing Model API is running."})

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    metrics = read_metrics()
    metrics["total_requests"] += 1
    metrics["last_request_timestamp"] = datetime.utcnow().isoformat()

    try:
        data = request.get_json()
        input_data = HousingInput(**data)

        input_df = pd.DataFrame([input_data.model_dump()])
        prediction = model.predict(input_df).tolist()

        # Prepare full result
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": input_data.model_dump(),
            "prediction": prediction
        }

        # Print input and output to console
        print("🔹 Prediction Request:")
        print(json.dumps(result, indent=2))

        # Append to predictions.json
        append_to_json_log(result)

        metrics["successful_requests"] += 1
        response_time = time.time() - start_time
        metrics["average_response_time"] = update_average_response_time(
            metrics["average_response_time"],
            response_time,
            metrics["successful_requests"]
        )

        write_metrics(metrics)
        return jsonify(result)

    except ValidationError as ve:
        metrics["failed_requests"] += 1
        write_metrics(metrics)
        return jsonify({"error": ve.errors()}), 422
    
    except Exception as e:
        metrics["failed_requests"] += 1
        write_metrics(metrics)
        return jsonify({"error": str(e)}), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = read_metrics()
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)
