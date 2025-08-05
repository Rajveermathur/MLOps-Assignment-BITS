from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError, Field
import pickle
import numpy as np
import pandas as pd
import joblib
import json
import os

# Initialize Flask app
app = Flask(__name__)

# Load the model
# with open('models/California_Housing_model.pkl', 'rb') as f:
    # model = pickle.load(f)
model = joblib.load('models/California_Housing_model.pkl')

# JSON log file path
LOG_FILE = 'log/predictions.json'

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

@app.route('/')
def home():
    return jsonify({"message": "California Housing Model API is running."})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = HousingInput(**data)

        input_df = pd.DataFrame([input_data.model_dump()])
        prediction = model.predict(input_df).tolist()

        # Prepare full result
        result = {
            # "input": input_data.dict(),
            "input": input_data.model_dump(),
            "prediction": prediction
        }

        # Print input and output to console
        print("🔹 Prediction Request:")
        print(json.dumps(result, indent=2))

        # Append to predictions.json
        append_to_json_log(result)

        return jsonify(result)

    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

if __name__ == '__main__':
    app.run(debug=True)
