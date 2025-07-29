import mlflow
import mlflow.sklearn
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import root_mean_squared_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

# Load California housing dataset
df = pd.read_csv('../data/cleaned_california_housing.csv')
X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Track experiments
mlflow.set_experiment("CaliforniaHousingModels")

best_rmse = float("inf")
best_run_id = None
best_model_name = None

def train_and_log_model(model, name, params={}):
    with mlflow.start_run(run_name=name) as run:
        # Set tags
        mlflow.set_tag("model_type", name)

        # Log params
        model.set_params(**params)
        all_params = model.get_params()
        mlflow.log_params(all_params)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Evaluate
        rmse = root_mean_squared_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(model, "model", registered_model_name=name)

        print(f"🔍 {name} RMSE: {rmse:.4f}")
        return run.info.run_id, rmse

# Train Linear Regression
lr = LinearRegression()
lr_run_id, lr_rmse = train_and_log_model(lr, "LinearRegression")

# Train Decision Tree
dt = DecisionTreeRegressor(random_state=42)
dt_run_id, dt_rmse = train_and_log_model(dt, "DecisionTree")

# Determine best
if lr_rmse < dt_rmse:
    best_rmse = lr_rmse
    best_run_id = lr_run_id
    best_model_name = "LinearRegression"
else:
    best_rmse = dt_rmse
    best_run_id = dt_run_id
    best_model_name = "DecisionTree"

print(f"✅ Best model: {best_model_name} with RMSE: {best_rmse:.4f}")

# Register best model in MLflow Model Registry
from mlflow import register_model
mlflow.register_model(
    model_uri=f"runs:/{best_run_id}/model",
    name="BestCaliforniaModel"
)