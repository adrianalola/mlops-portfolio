import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pythonjsonlogger import jsonlogger

from app.model import model_manager
from app.schemas import PredictionRequest, PredictionResponse, HealthResponse

# ── Logging setup ──────────────────────────────────────────────────────────────
# JSON logs are easier to parse in CloudWatch
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

# ── Lifespan: runs on startup and shutdown ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP — load model before accepting any requests
    logger.info("Starting up — loading model...")
    model_manager.load()
    logger.info("Model loaded. API is ready.")
    yield
    # SHUTDOWN
    logger.info("Shutting down.")

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Cancer Detection MLOps API",
    description="Breast cancer classification model served via FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
def health_check():
    """
    Health check endpoint.
    Used by load balancers and monitoring tools to verify the API is alive.
    """
    return {
        "status": "ok",
        "model_loaded": model_manager.is_loaded,
        "environment": os.environ.get("APP_ENV", "development")
    }

@app.get("/info", tags=["Monitoring"])
def model_info():
    """
    Returns metadata about the loaded model.
    Useful for debugging and auditing which model version is running.
    """
    return model_manager.metadata

@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
def predict(request: PredictionRequest):
    """
    Run inference on a single sample.
    Send 30 numeric features, get back a prediction (malignant/benign).
    """
    if not model_manager.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    try:
        result = model_manager.predict([request.features])
        logger.info("prediction_made", extra={
            "label": result["results"][0]["label"],
            "confidence": result["results"][0]["confidence"]
        })
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
