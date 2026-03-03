from fastapi import FastAPI, Request
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List
from app.rules import calculate_risk

import logging
import time
from prometheus_client import Counter, Histogram, generate_latest

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Prometheus Metrics
# --------------------------------------------------

REQUEST_COUNT = Counter(
    "api_request_count",
    "Total number of API requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency in seconds",
    ["endpoint"]
)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Telecom Churn Risk API - Stage 1 (DevOps)",
    description="Rule-Based Churn Risk Prediction System",
    version="1.0"
)

# --------------------------------------------------
# Request Models
# --------------------------------------------------

class Ticket(BaseModel):
    date: str
    category: str


class Customer(BaseModel):
    customer_id: str
    contract_type: str
    monthly_charge_change: float


class RiskRequest(BaseModel):
    customer: Customer
    tickets: List[Ticket]

# --------------------------------------------------
# Middleware for Metrics
# --------------------------------------------------

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(duration)

    return response

# --------------------------------------------------
# Health Check Endpoint
# --------------------------------------------------

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

# --------------------------------------------------
# Predict Risk Endpoint
# --------------------------------------------------

@app.post("/predict-risk")
def predict_risk(data: RiskRequest):
    logger.info(f"Received request for customer {data.customer.customer_id}")

    risk = calculate_risk(
        data.customer.dict(),
        [ticket.dict() for ticket in data.tickets]
    )

    logger.info(f"Risk predicted: {risk}")

    return {
        "customer_id": data.customer.customer_id,
        "risk_category": risk
    }

# --------------------------------------------------
# Prometheus Metrics Endpoint
# --------------------------------------------------

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
