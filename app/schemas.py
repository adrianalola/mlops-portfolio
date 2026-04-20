from pydantic import BaseModel, Field
from typing import List

class PredictionRequest(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=30,
        max_length=30,
        description="30 numeric features from the breast cancer dataset"
    )

class ConfidenceScore(BaseModel):
    malignant: float
    benign: float

class PredictionResult(BaseModel):
    prediction: int
    label: str
    confidence: ConfidenceScore

class PredictionResponse(BaseModel):
    results: List[PredictionResult]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    environment: str
