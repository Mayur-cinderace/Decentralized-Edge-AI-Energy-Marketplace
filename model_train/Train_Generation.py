# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import joblib

# 2. Load Data
df = pd.read_csv("Solar_Data.csv")

# 3. Display Data Overview
print(df.head())
print(df.info())
print(df.describe())

# 4. Handle Missing Values
df = df.dropna()

# 5. Define Features and Target
X = df[['IRRADIATION','AMBIENT_TEMPERATURE','MODULE_TEMPERATURE',
        'hour_sin','hour_cos','minute_sin','minute_cos']]
y = df['AC_POWER']

# 6. Split Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Train Random Forest Model
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# 👉 7A. Save Model as .pkl
joblib.dump(model, "solar_rf_model.pkl")
print("Model saved as solar_rf_model.pkl")

# 8. Predict
y_pred = model.predict(X_test)

# 9. Evaluate Model
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
mean_power = df['AC_POWER'].mean()
normalized_rmse = rmse / mean_power

print(f"Normalized RMSE: {normalized_rmse:.2%}")
print(f"RMSE: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

# 10. Feature Importance Visualization
plt.figure(figsize=(8, 6))
importances = model.feature_importances_
plt.bar(X.columns, importances)
plt.title("Feature Importance (Random Forest)")
plt.xticks(rotation=45)
plt.show()

# 11. Plot Actual vs Predicted
plt.figure(figsize=(7, 5))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.xlabel("Actual Power Output")
plt.ylabel("Predicted Power Output")
plt.title("Actual vs Predicted Power Output (Random Forest)")
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.show()
