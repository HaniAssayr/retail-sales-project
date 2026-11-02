import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load weekly revenue
df = pd.read_csv("weekly_revenue.csv", parse_dates=["Week"])
df = df.sort_values("Week").reset_index(drop=True)

# Create features using previous weeks only
df["previous_week"] = df["Revenue"].shift(1)
df["previous_4_week_avg"] = (
    df["Revenue"].shift(1).rolling(window=4).mean()
)

# Remove rows without enough previous data
df = df.dropna().reset_index(drop=True)

# Chronological 80/20 split
split_index = int(len(df) * 0.8)
train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

features = ["previous_week", "previous_4_week_avg"]
X_train = train[features]
y_train = train["Revenue"]
X_test = test[features]
y_test = test["Revenue"]

# Baseline: last revenue observed in training
baseline_predictions = np.repeat(
    y_train.iloc[-1], len(test)
)

# Random Forest
rf_model = RandomForestRegressor(
    n_estimators=200, random_state=42
)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_predictions = linear_model.predict(X_test)

# Evaluate models
predictions = {
    "Baseline": baseline_predictions,
    "Random Forest": rf_predictions,
    "Linear Regression": linear_predictions,
}

for name, pred in predictions.items():
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    print(f"{name}: MAE = {mae:.2f}, RMSE = {rmse:.2f}")



# Investigate forecast errors
error_analysis = pd.DataFrame({
    "Week": test["Week"].values,
    "Actual": y_test.values,
    "Baseline_Prediction": baseline_predictions,
    "RandomForest_Prediction": rf_predictions,
    "LinearRegression_Prediction": linear_predictions
})

# To Calculate prediction errors
for model in ["Baseline", "RandomForest", "LinearRegression"]:
    error_analysis[f"{model}_Error"] = (
        error_analysis[f"{model}_Prediction"] - error_analysis["Actual"]
    )

    error_analysis[f"{model}_Absolute_Error"] = (
        error_analysis[f"{model}_Error"].abs()
    )

print("\nFORECAST ERROR ANALYSIS")
print(
    error_analysis.to_string(
        index=False,
        formatters={
            col: lambda x: f"{x:.2f}"
            for col in error_analysis.select_dtypes(
                include="number"
            ).columns
        }
    )
)

# Find the worst prediction for each model
print("\nLARGEST FORECAST ERRORS")

for model in ["Baseline", "RandomForest", "LinearRegression"]:
    worst = error_analysis.loc[
        error_analysis[f"{model}_Absolute_Error"].idxmax()
    ]

    print(
        f"{model}: Week = {worst['Week']}, "
        f"Actual = {worst['Actual']:.2f}, "
        f"Predicted = {worst[f'{model}_Prediction']:.2f}, "
        f"Absolute Error = {worst[f'{model}_Absolute_Error']:.2f}"
    )

# Plot forecast errors
plt.figure(figsize=(12, 6))

plt.plot(
    error_analysis["Week"],
    error_analysis["Baseline_Error"],
    marker="o",
    label="Baseline"
)

plt.plot(
    error_analysis["Week"],
    error_analysis["RandomForest_Error"],
    marker="o",
    label="Random Forest"
)

plt.plot(
    error_analysis["Week"],
    error_analysis["LinearRegression_Error"],
    marker="o",
    label="Linear Regression"
)

plt.axhline(y=0, linestyle="--")

plt.title("Weekly Revenue Forecast Errors")
plt.xlabel("Week")
plt.ylabel("Prediction Error (£)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("forecast_errors.png")
plt.show()

# Load weekly revenue data
weekly_revenue = pd.read_csv(
    BASE_DIR / "weekly_revenue.csv",
    parse_dates=["Week"]
)
weekly_revenue = weekly_revenue.sort_values("Week").reset_index(drop=True)

# Chronological 80/20 split
split_index = int(len(weekly_revenue) * 0.8)

train = weekly_revenue.iloc[:split_index].copy()
test = weekly_revenue.iloc[split_index:].copy()

# Create time-based features
for data in (train, test):
    data["week_number"] = data["Week"].dt.isocalendar().week.astype(int)
    data["month"] = data["Week"].dt.month
    data["time_index"] = np.arange(len(data))

# Continue time index into the test period
test["time_index"] = np.arange(len(train), len(train) + len(test))

features = ["week_number", "month", "time_index"]

X_train = train[features]
y_train = train["Revenue"]

X_test = test[features]
y_test = test["Revenue"]

# Baseline forecast: last training week's revenue
baseline_predictions = np.repeat(y_train.iloc[-1], len(test))

# Random Forest model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)
rf_predictions = model.predict(X_test)

# Evaluate both approaches
predictions = {
    "Baseline": baseline_predictions,
    "Random Forest": rf_predictions
}

print("\nMODEL EVALUATION")

for name, pred in predictions.items():
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))

    print(f"{name}: MAE = {mae:.2f}, RMSE = {rmse:.2f}")

# Investigate forecast errors
error_analysis = pd.DataFrame({
    "Week": test["Week"].values,
    "Actual": y_test.values,
    "Baseline_Prediction": baseline_predictions,
    "RandomForest_Prediction": rf_predictions
})

for name in ["Baseline", "RandomForest"]:
    error_analysis[f"{name}_Error"] = (
        error_analysis[f"{name}_Prediction"] - error_analysis["Actual"]
    )

    error_analysis[f"{name}_Absolute_Error"] = (
        error_analysis[f"{name}_Error"].abs()
    )

print("\nFORECAST ERROR ANALYSIS")
print(error_analysis.round(2).to_string(index=False))

# Forecast comparison chart
plt.figure(figsize=(12, 6))

plt.plot(
    test["Week"], y_test,
    label="Actual Revenue", marker="o"
)

plt.plot(
    test["Week"], baseline_predictions,
    label="Baseline Forecast", linestyle="--"
)

plt.plot(
    test["Week"], rf_predictions,
    label="Random Forest", linestyle="--"
)

plt.title("Actual vs Predicted Weekly Revenue")
plt.xlabel("Week")
plt.ylabel("Revenue (£)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(BASE_DIR / "outputs" / "forecast_comparison.png")
plt.close()
