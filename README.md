# California Housing Price Prediction API 🏡

This is a Flask-based REST API that serves predictions from a trained model on the California Housing dataset.

## 🚀 How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Start the server:
    ```bash
    python flask_app.py
    ```

3. Test the API:

    - Endpoint: `POST /predict`
    - Sample input:
      ```json
      {
        "MedInc": 8.3252,
        "HouseAge": 41.0,
        "AveRooms": 6.9841,
        "AveBedrms": 1.0238,
        "Population": 322.0,
        "AveOccup": 2.5556,
        "Latitude": 37.88,
        "Longitude": -122.23
      }
      ```

4. Prediction and input logs are saved to `predictions.json`.

## 🧠 Dependencies

- Flask
- scikit-learn
- pydantic
- pandas
