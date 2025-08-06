# 🧠 MLOps-Assignment

A complete **end-to-end Machine Learning pipeline** built with best practices using:

- **📦 DVC** for dataset versioning  
- **📝 MLFlow** for experiment tracking and model registry  
- **🤖 ML Models**: Linear Regression & Decision Tree  
- **🐳 Docker** for containerization
- **⚙️ GitHub Actions** for CI/CD automation 
- **📦 Flask** for API development
- **📈 Dash** for interactive visualizations
- **📊 Prometheus** for monitoring

## 🚀 Features

### 🔁 Data Versioning with DVC

- Tracks raw and processed datasets
- Enables reproducibility across versions

### 🧠 Model Training & Tracking

- Trains models (Linear Regression and Decision Tree) on California Housing dataset
- Logs:
  - 📊 Parameters
  - 📈 Metrics (MAE, R², RMSE)
  - 🧠 Model artifacts
- Registers models to MLFlow

### ⚙️ CI/CD with GitHub Actions

- Automatically runs `training.py` on each `push` to `main`
- Commits updated `mlruns/` and results back to the repo
- Builds and pushes Docker image to Docker Hub

### 📦 Docker Containerization
 
- Dockerfile for containerizing the application
- Runs Flask API, MLFlow server, and Dash app in a single container
- Exposes ports for:
  - Flask API: 5000
  - MLFlow UI: 5001
  - Dash app: 8050
  - Prometheus metrics: 8000

### 📈 Monitoring with Prometheus

- Exposes model performance metrics at `/metrics`
- Provides insights into:
  - Model performance (MAE, R², RMSE)
  - Training parameters
  - Prediction logs

### 📊 Interactive Visualizations with Dash
- Provides an interactive dashboard at `/`
- Visualizes:
  - Sucessful predictions
  - Last API call

---

## Setup & Running the Project 🏡

## Local Run

### Setup Python
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- Run servers::`./run.sh`

### Docker Run
- Pull latest image: `docker pull 2023ac05022divyansh/mlops-g15-a1`
- Verify image pull: `docker images`
- Run Container: `docker run -p 5000:5000 -p 8000:8000 -p 8050:8050 2023ac05022divyansh/mlops-g15-a1`

Test the APIs:
- 
- Endpoint: `[POST] localhost:5000/predict` 

- Sample input:
  ```
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

**Prediction and input logs are saved to `predictions.json`.**

- Endpoint: `[GET] localhost:8000/metrics`
- Returns: Prometheus metrics for monitoring
  - Model performance metrics
  - Training parameters
  - Prediction logs

- Endpoint: `[GET] localhost:8050/`
- Returns:
  - Model performance dashboard
  - Interactive visualizations

- Endpoint: `[GET] localhost:5000/metrics`
- Returns:
  - Model metrics (MAE, R², RMSE)
  - Model parameters
  - Prediction logs

- Endpoint: `[GET] localhost:5001`
- Returns: Mlflow UI for experiment tracking and model registry
  - Experiment runs
  - Model versions
  - Metrics and parameters