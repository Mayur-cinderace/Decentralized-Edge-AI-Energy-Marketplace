import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import joblib

# ---------------------------------------------
# Step 1: Load OPSD consumption dataset
# ---------------------------------------------
df = pd.read_csv("Consumer_Solar.csv")

# Convert timestamps
df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"])

# ---------------------------------------------
# Step 2: Automatically detect all "actual load" columns
# ---------------------------------------------
consumption_cols = [c for c in df.columns if c.endswith("_load_actual_entsoe_transparency")]

print("Detected consumer consumption columns:")
print(consumption_cols)

# Remove rows with no consumption data at all
df[consumption_cols] = df[consumption_cols].fillna(0)

# Create a single consumption index feature
df["CONSUMPTION_INDEX"] = df[consumption_cols].mean(axis=1)

# ---------------------------------------------
# Step 3: Feature engineering
# ---------------------------------------------
df["HOUR"] = df["utc_timestamp"].dt.hour
df["DAY"] = df["utc_timestamp"].dt.day
df["MONTH"] = df["utc_timestamp"].dt.month

# Features (simple for API)
X = df[["HOUR", "DAY", "MONTH"]]
y = df["CONSUMPTION_INDEX"]

# ---------------------------------------------
# Step 4: Train-test split
# ---------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------------------
# Step 5: Train consumer model
# ---------------------------------------------
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=18,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, preds))

# ---------------------------------------------
# Step 6: Graph — Actual vs Predicted (same plot)
# ---------------------------------------------
plt.figure(figsize=(10, 5))

# Plot actual consumption (first 300 samples)
plt.plot(y_test.values[:300], label="Actual Consumption")

# Plot predicted consumption
plt.plot(preds[:300], label="Predicted Consumption")

plt.title("Actual vs Predicted Consumer Load (Sample of 300 Points)")
plt.xlabel("Time Index (Sample)")
plt.ylabel("Consumption Index")
plt.legend()
plt.grid(True)
plt.show()

# ---------------------------------------------
# Step 7: Save consumer model
# ---------------------------------------------
joblib.dump(model, "consumer_load_model.pkl")

print("Saved consumer_load_model.pkl")
