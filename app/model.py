import os
import logging
from typing import List

import joblib
import numpy as np

logger = logging.getLogger(__name__)

LOCAL_MODEL_DIR = "model_artifacts"
MODEL_FILENAME = "cancer_model.joblib"
FEATURES_FILENAME = "feature_names.joblib"
CLASS_LABELS = {0: "malignant", 1: "benign"}

class ModelManager:
    def __init__(self):
        self.model = None
        self.feature_names: List[str] = []
        self.is_loaded: bool = False

    def load(self) -> None:
        model_path = os.path.join(LOCAL_MODEL_DIR, MODEL_FILENAME)
        features_path = os.path.join(LOCAL_MODEL_DIR, FEATURES_FILENAME)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Run train.py first.")

        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(features_path)
        self.is_loaded = True
        logger.info(f"Model loaded. Features: {len(self.feature_names)}")

    def predict(self, features: List[List[float]]) -> dict:
        if not self.is_loaded:
            raise RuntimeError("Model not loaded.")

        X = np.array(features)

        if X.shape[1] != len(self.feature_names):
            raise ValueError(
                f"Expected {len(self.feature_names)} features, got {X.shape[1]}"
            )

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        results = []
        for pred, prob in zip(predictions, probabilities):
            results.append({
                "prediction": int(pred),
                "label": CLASS_LABELS[int(pred)],
                "confidence": {
                    "malignant": round(float(prob[0]), 4),
                    "benign": round(float(prob[1]), 4),
                }
            })
        return {"results": results}

    @property
    def metadata(self) -> dict:
        if not self.is_loaded:
            return {"status": "not_loaded"}
        return {
            "status": "loaded",
            "num_features": len(self.feature_names),
            "feature_names": self.feature_names,
            "classes": CLASS_LABELS,
        }

model_manager = ModelManager()
