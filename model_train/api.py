from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model + encoder
bundle = joblib.load("solar_combined_model.pkl")
model = bundle["model"]
label_encoder = bundle["label_encoder"]

class PredictionInput(BaseModel):
    ambient_temp: float
    module_temp: float
    irradiation: float
    hour: int
    day: int
    month: int
    source_key: str

app = FastAPI()

@app.post("/predict")
def predict(data: PredictionInput):

    print("Received data:", data)

    if data.source_key not in label_encoder.classes_:
        print("Unknown source key:", data.source_key)
        return {"error": "Unknown SOURCE_KEY"}

    encoded_source = label_encoder.transform([data.source_key])[0]
    print("Encoded source:", encoded_source)

    features = np.array([[ 
        data.ambient_temp,
        data.module_temp,
        data.irradiation,
        data.hour,
        data.day,
        data.month,
        encoded_source
    ]])

    print("Feature vector:", features)

    pred = model.predict(features)[0]
    print("Prediction:", pred)

    return {"predicted_dc_power": float(pred)}


@app.get("/")
def home():
    return {"message": "Solar Prediction API is running!"}
