import joblib
import os

MODEL_PATH = os.path.join("ml", "model.pkl")

model = joblib.load(MODEL_PATH)

def predict(features):
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1]
    return int(prediction), float(probability)
