from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.model_loader import predict
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Telecom Churn Risk API - Stage 2 (ML Version)",
    description="Machine Learning Based Churn Prediction",
    version="2.0"
)

class PredictionRequest(BaseModel):
    features: List[float]

@app.post("/predict-risk")
def predict_risk(data: PredictionRequest):
    logging.info("ML prediction request received")

    prediction, probability = predict(data.features)

    return {
        "churn_prediction": prediction,
        "churn_probability": probability
    }

@app.get("/health")
def health_check():
    return {"status": "healthy-ml"}
