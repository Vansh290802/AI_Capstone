from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import joblib
import pandas as pd
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger
from utils.monitor import PerformanceMonitor

# Initialize FastAPI app
app = FastAPI(title="Revenue Prediction API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logger and monitor
logger = setup_logger()
monitor = PerformanceMonitor()

class PredictionRequest(BaseModel):
    country: str
    date: str
    features: Dict[str, float]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/predict/{country}")
async def predict_country(country: str):
    """Predict revenue for specific country"""
    try:
        model = joblib.load('../models/revenue_model.joblib')
        prediction = {"country": country, "predicted_revenue": 0}  # Placeholder
        monitor.log_prediction(country, prediction)
        return prediction
    except Exception as e:
        logger.error(f"Prediction error for {country}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict/all")
async def predict_all():
    """Predict revenue for all countries"""
    try:
        model = joblib.load('../models/revenue_model.joblib')
        predictions = []  # Placeholder
        monitor.log_bulk_prediction(len(predictions))
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Bulk prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    """Get model performance metrics"""
    return monitor.get_metrics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
