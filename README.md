# 🧠 MLOps-Assignment-BITS

A complete **end-to-end Machine Learning pipeline** built with best practices using:

- **📦 DVC** for dataset versioning  
- **📝 MLflow** for experiment tracking and model registry  
- **🤖 ML Models**: Linear Regression & Decision Tree  
- **⚙️ GitHub Actions** for CI/CD automation 

## 🚀 Features

### 🔁 Data Versioning with DVC

- Tracks raw and processed datasets
- Enables reproducibility across versions

### 🧠 Model Training & Tracking

- Trains models on California Housing dataset
- Logs:
  - 📊 Parameters
  - 📈 Metrics (MAE, R²)
  - 🧠 Model artifacts
- Registers best model to MLflow

### ⚙️ CI/CD with GitHub Actions

- Automatically runs `training.py` on each `push` to `main`
- Commits updated `mlruns/` and results back to the repo

---

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

---
## Local Run
### Setup Python
- `python3 -m venv venv`
- `source venv/bin/activate`
- Run app server::`python main.py`
- Run app server using uvicorn

### Docker
- `docker build -t fastapi-hello .`
- `docker run -p 8000:8000 fastapi-hello`