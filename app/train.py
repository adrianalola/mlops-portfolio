import os
import joblib
import logging
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, classification_report
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def train_and_save_model(output_dir="model_artifacts"):
    mlflow.set_tracking_uri("mlruns")
    mlflow.set_experiment("cancer-detection")

    with mlflow.start_run():
        logger.info("Loading Breast Cancer dataset...")
        data = load_breast_cancer()
        X, y = data.data, data.target
        feature_names = data.feature_names.tolist()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        params = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
        mlflow.log_params(params)

        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(**params, n_jobs=-1))
        ])

        logger.info("Training model...")
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        metrics = {
            "accuracy":  accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall":    recall_score(y_test, y_pred),
            "f1_score":  f1_score(y_test, y_pred)
        }
        mlflow.log_metrics(metrics)

        for k, v in metrics.items():
            logger.info(f"{k}: {v:.4f}")
        logger.info("\n" + classification_report(y_test, y_pred, target_names=data.target_names))

        os.makedirs(output_dir, exist_ok=True)
        joblib.dump(pipeline, os.path.join(output_dir, "cancer_model.joblib"))
        joblib.dump(feature_names, os.path.join(output_dir, "feature_names.joblib"))
        mlflow.sklearn.log_model(pipeline, "model")

        logger.info("Model saved. MLflow run complete!")

if __name__ == "__main__":
    train_and_save_model()
