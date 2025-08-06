# 🧠 MLOps-Assignment-BITS

A complete **end-to-end Machine Learning pipeline** built with best practices using:

- **📦 DVC** for dataset versioning  
- **📝 MLFlow** for experiment tracking and model registry  
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
- Registers best model to MLFlow

### ⚙️ CI/CD with GitHub Actions

- Automatically runs `training.py` on each `push` to `main`
- Commits updated `mlruns/` and results back to the repo

---

# California Housing Price Prediction API 🏡

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

Test the API:
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