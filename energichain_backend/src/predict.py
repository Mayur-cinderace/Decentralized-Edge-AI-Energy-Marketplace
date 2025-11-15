import pickle
import pandas as pd
import numpy as np
import sys
import json
from datetime import datetime

# Load the model
with open("solar_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

def calculate_time_features(date_time_str):
    """Calculate sinusoidal time features from datetime string."""
    dt = datetime.fromisoformat(date_time_str.replace("T", " "))
    hour = dt.hour
    minute = dt.minute
    return {
        "hour_sin": np.sin(2 * np.pi * hour / 24),
        "hour_cos": np.cos(2 * np.pi * hour / 24),
        "minute_sin": np.sin(2 * np.pi * minute / 60),
        "minute_cos": np.cos(2 * np.pi * minute / 60)
    }

def predict(data):
    try:
        date_time = data["dateTime"]
        irradiation = float(data["irradiation"])
        ambient_temp = float(data["ambientTemp"])
        module_temp = float(data["moduleTemp"])

        # Validate inputs
        if irradiation < 0 or irradiation > 1500:
            return {"error": "Irradiation should be between 0-1500 W/m²"}
        if ambient_temp < -50 or ambient_temp > 100:
            return {"error": "Ambient temperature out of range"}
        if module_temp < -50 or module_temp > 100:
            return {"error": "Module temperature out of range"}

        # Calculate time features
        time_features = calculate_time_features(date_time)

        # Prepare features
        features = pd.DataFrame([{
            "IRRADIATION": irradiation,
            "AMBIENT_TEMPERATURE": ambient_temp,
            "MODULE_TEMPERATURE": module_temp,
            "hour_sin": time_features["hour_sin"],
            "hour_cos": time_features["hour_cos"],
            "minute_sin": time_features["minute_sin"],
            "minute_cos": time_features["minute_cos"]
        }])

        # Make prediction
        predicted_power = model.predict(features)[0]
        predicted_power = max(0, float(predicted_power))  # Ensure non-negative

        return {
            "predictedPower": round(predicted_power, 2),
            "irradiation": irradiation,
            "ambientTemp": ambient_temp,
            "moduleTemp": module_temp,
            "time": date_time
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Read input from stdin (sent by Node.js)
    input_data = json.load(sys.stdin)
    result = predict(input_data)
    # Output result as JSON to stdout
    print(json.dumps(result))