import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import root_mean_squared_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import joblib
import numpy as np

# Load California housing dataset
df = pd.read_csv('data/cleaned_california_housing.csv')
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
        mlflow.log_params(params)

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Evaluate
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mlflow.log_metric("rmse", rmse)

        # Log model to MLflow
        mlflow.sklearn.log_model(model, "model", registered_model_name=name)

        print(f"🔍 {name} RMSE: {rmse:.4f}")
        return run.info.run_id, rmse, model

# Train Linear Regression
lr = LinearRegression()
lr_run_id, lr_rmse, lr_model = train_and_log_model(lr, "LinearRegression")

# Train Decision Tree
dt = DecisionTreeRegressor(random_state=42)
dt_run_id, dt_rmse, dt_model = train_and_log_model(dt, "DecisionTree")


# Determine best
if lr_rmse < dt_rmse:
    best_rmse = lr_rmse
    best_run_id = lr_run_id
    best_model_name = "LinearRegression"
    best_model = lr_model
else:
    best_rmse = dt_rmse
    best_run_id = dt_run_id
    best_model_name = "DecisionTree"
    best_model = dt_model

os.makedirs("models", exist_ok=True)
# Save best model to root directory with custom name
joblib.dump(best_model, "models/California_Housing_model.pkl")

print(f"✅ Best model: {best_model_name} with RMSE: {best_rmse:.4f}")
print(f"💾 Saved as: California_Housing_model.pkl")

# Register best model in MLflow Model Registry
from mlflow import register_model
mlflow.register_model(
    model_uri=f"runs:/{best_run_id}/model",
    name="BestCaliforniaModel"
)