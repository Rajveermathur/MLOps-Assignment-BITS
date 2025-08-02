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

## Local Run
### Setup Python
- `python3 -m venv venv`
- `source venv/bin/activate`
- Run app server::`python main.py`
- Run app server using uvicorn

### Docker
- `docker build -t fastapi-hello .`
- `docker run -p 8000:8000 fastapi-hello`