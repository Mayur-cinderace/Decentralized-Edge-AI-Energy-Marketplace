import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import joblib

# ---------------------------------------------
# Step 1: Load CSVs
# ---------------------------------------------
p1_gen = pd.read_csv("Plant_1_Generation_Data.csv")
p1_weather = pd.read_csv("Plant_1_Weather_Sensor_Data.csv")

# Convert DATE_TIME
for df in [p1_gen, p1_weather]:
    df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"], dayfirst=True)

# Merge
p1 = p1_gen.merge(p1_weather, on=["DATE_TIME", "PLANT_ID"])
df = pd.concat([p1]).dropna()

# Feature engineering
df["HOUR"] = df["DATE_TIME"].dt.hour
df["DAY"] = df["DATE_TIME"].dt.day
df["MONTH"] = df["DATE_TIME"].dt.month

# Encode
le = LabelEncoder()
df["SOURCE_ENCODED"] = le.fit_transform(df["SOURCE_KEY_x"])

# Features + target
features = [
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION",
    "HOUR",
    "DAY",
    "MONTH",
    "SOURCE_ENCODED"
]
target = "AC_POWER"

X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=18,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Predict
preds = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, preds))
print("R2 Score:", r2_score(y_test, preds))

# ---------------------------------------------
# PLOT BOTH LINES IN ONE GRAPH
# ---------------------------------------------
plt.figure(figsize=(10, 5))

# Plot actual values
plt.plot(y_test[:300].values, label="Actual AC Power")

# Plot predicted values
plt.plot(preds[:300], label="Predicted AC Power")

plt.title("Actual vs Predicted AC Power (Sample of 300 Points)")
plt.xlabel("Time Index (Sample)")
plt.ylabel("AC Power")
plt.legend()         # <-- This makes it clear which is which
plt.grid(True)
plt.show()

# Save model
joblib.dump({"model": model, "label_encoder": le}, "solar_combined_model.pkl")
print("Saved solar_combined_model.pkl")