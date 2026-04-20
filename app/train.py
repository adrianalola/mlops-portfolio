import os
import joblib
import logging
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

def train_and_save_model(output_dir="model_artifacts"):
    logger.info("Loading Breast Cancer dataset...")
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = data.feature_names.tolist()
    logger.info(f"Dataset shape: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info(f"Train: {len(X_train)} | Test: {len(X_test)}")

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        ))
    ])

    logger.info("Training model...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    logger.info("\n" + classification_report(y_test, y_pred, target_names=data.target_names))

    if accuracy < 0.90:
        raise ValueError(f"Accuracy {accuracy:.2f} below threshold 0.90")

    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(pipeline, os.path.join(output_dir, "cancer_model.joblib"))
    joblib.dump(feature_names, os.path.join(output_dir, "feature_names.joblib"))
    logger.info("Model saved to model_artifacts/")

if __name__ == "__main__":
    train_and_save_model()
