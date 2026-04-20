# 🚀 MLOps Portfolio Project

An end-to-end MLOps pipeline built with AWS, Docker, Terraform, and GitHub Actions.
Demonstrates production-grade ML infrastructure for a breast cancer classification model.

---

## 📋 Table of Contents

1. [Architecture](#-architecture)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Quick Start](#-quick-start)
5. [API Endpoints](#-api-endpoints)
6. [Experiment Tracking with MLflow](#-experiment-tracking-with-mlflow)
7. [AWS Infrastructure](#-aws-infrastructure)
8. [CI/CD Pipeline](#-cicd-pipeline)
9. [Model Performance](#-model-performance)
10. [Roadmap & Future Improvements](#-roadmap--future-improvements)
11. [Author](#-author)

---

## 🏗️ Architecture

```
GitHub Actions (CI/CD)
        │
        ▼
   Docker Image
        │
        ▼
  AWS EC2 Instance ◄──── AWS IAM Role
        │                      │
        ▼                      ▼
   FastAPI REST API      AWS S3 Bucket
        │               (model artifacts)
        ▼
  scikit-learn Model
  (tracked with MLflow)
```


---



## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| ML Model | scikit-learn (Random Forest) |
| Experiment Tracking | MLflow |
| REST API | FastAPI + Uvicorn |
| Containerization | Docker |
| Cloud Provider | AWS (EC2, S3, IAM) |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Language | Python 3.11 |

---

## 📁 Project Structure

```
mlops-portfolio/
├── app/
│   ├── main.py          # FastAPI application
│   ├── model.py         # Model loading & prediction logic
│   ├── schemas.py       # Pydantic input/output schemas
│   └── train.py         # Training script with MLflow tracking
├── model_artifacts/     # Saved model files (uploaded to S3)
├── infrastructure/
│   ├── main.tf          # AWS resources (EC2, S3, IAM, Security Groups)
│   ├── variables.tf     # Terraform variables
│   ├── outputs.tf       # Terraform outputs
│   └── user_data.sh     # EC2 startup script
├── .github/
│   └── workflows/
│       └── deploy.yml   # CI/CD pipeline
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/adrianalola/mlops-portfolio.git
cd mlops-portfolio
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Train the model
```bash
python app/train.py
```

### 4. View experiment tracking
```bash
mlflow ui --port 5001
# Open http://127.0.0.1:5001
```

### 5. Run the API locally
```bash
uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000/docs
```

### 6. Run with Docker
```bash
docker build -t mlops-cancer-api .
docker run -p 8000:8000 mlops-cancer-api
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check — model status |
| GET | `/info` | Model metadata and features |
| POST | `/predict` | Run inference |

### Example prediction request
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776,
                 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053,
                 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587,
                 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0,
                 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
  }'
```

### Example response
```json
{
  "results": [{
    "prediction": 0,
    "label": "malignant",
    "confidence": {
      "malignant": 0.97,
      "benign": 0.03
    }
  }]
}
```

---

## 📈 Experiment Tracking with MLflow

All training runs are tracked locally with **MLflow** inside the `mlruns/` folder.

Every time you run `python app/train.py` MLflow automatically records:

| What | Example |
|------|---------|
| Parameters | n_estimators=100, max_depth=10, random_state=42 |
| Metrics | accuracy=0.956, precision=0.959, recall=0.972, f1=0.965 |
| Model artifact | sklearn pipeline saved |
| Duration | 3.2s |
| Source | train.py |

To view the UI:
```bash
mlflow ui --port 5001
# Open http://127.0.0.1:5001
```

To compare experiments, change a parameter in `train.py` and run it again — MLflow saves every run separately so you can see which parameters gave the best results.

---

## ☁️ AWS Infrastructure

Provisioned with Terraform:

- **EC2** (t2.micro) — hosts the Docker container
- **S3 Bucket** — stores trained model artifacts
- **IAM Role** — least privilege access (S3 read-only)
- **Security Group** — allows port 8000 (API) and 22 (SSH)

### Deploy infrastructure
```bash
cd infrastructure
terraform init
terraform apply
```

### Destroy infrastructure (to avoid costs)
```bash
terraform destroy
```

---

## 🔄 CI/CD Pipeline

Automated with **GitHub Actions** — workflow file at `.github/workflows/deploy.yml`

Every push to `main` automatically:

1. Connects to EC2 via SSH using stored secrets
2. Pulls latest code from GitHub
3. Downloads model artifacts from S3
4. Builds fresh Docker image on the server
5. Stops old container and starts new one with zero downtime

Secrets required in GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `EC2_HOST` | Public IP of the EC2 instance |
| `EC2_SSH_KEY` | Private SSH key to connect to EC2 |
| `AWS_ACCESS_KEY_ID` | AWS credentials for CLI access |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials for CLI access |

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 95.6% |
| Precision | 95.9% |
| Recall | 97.2% |
| F1 Score | 96.5% |

Dataset: [Breast Cancer Wisconsin](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html)
— 569 samples, 30 features, binary classification (malignant/benign)
<img width="1463" height="873" alt="Captura de pantalla 2026-04-20 a la(s) 23 39 42" src="https://github.com/user-attachments/assets/6c3e98ce-e74c-444e-ab4a-9aa5b68f8659" />


---

## 🗺️ Roadmap & Future Improvements

This project is intentionally scoped to demonstrate core MLOps infrastructure skills.
The following improvements reflect a natural evolution toward enterprise-grade MLOps.

### ⚡ Short Term — Low/No Cost

| Improvement | Description |
|-------------|-------------|
| **CloudWatch Integration** | Ship container logs to AWS CloudWatch for centralized monitoring and alerting |
| **Model Versioning** | Tag MLflow runs with Git commit SHA to link every model version to its exact code |
| **Input Data Validation** | Add stricter feature range checks and anomaly detection on incoming requests |
| **Unit & Integration Tests** | Add pytest coverage for model loading, prediction logic, and API endpoints |
| **Docker Multi-stage Build** | Reduce final image size by separating build and runtime stages |

### 🚀 Medium Term — Moderate Complexity

| Improvement | Description |
|-------------|-------------|
| **AWS ECR** | Push Docker images to Elastic Container Registry instead of building on EC2 directly |
| **Application Load Balancer** | Add ALB in front of EC2 for HTTPS, health checks, and zero-downtime deploys |
| **Auto Scaling Group** | Scale EC2 instances automatically based on API traffic |
| **Feature Store** | Centralize and version input features using AWS Feature Store or Feast |
| **Data Drift Detection** | Monitor incoming request distributions and alert when they diverge from training data |

### 🏢 Enterprise Grade — AWS SageMaker

> ⚠️ **Note:** SageMaker is the AWS-native MLOps platform used in production at scale.
> It is intentionally excluded from this project due to cost — SageMaker endpoints,
> notebooks, and pipelines are not covered by the AWS Free Tier.
> The architecture below represents the next evolution of this project in a professional setting.

| SageMaker Component | What It Replaces In This Project |
|--------------------|----------------------------------|
| **SageMaker Pipelines** | Manual `python train.py` + GitHub Actions training step |
| **SageMaker Model Registry** | Local MLflow model tracking |
| **SageMaker Endpoints** | FastAPI on EC2 |
| **SageMaker Model Monitor** | Manual monitoring / no drift detection |
| **SageMaker Feature Store** | Raw features passed directly to API |

Migrating this project to SageMaker would be a natural next step in a production AWS environment and is part of the planned learning path for this portfolio.

---

## 👩‍💻 Author

**Adriana** — Cloud & DevOps Engineer transitioning into MLOps and QDevOps

> Specializing in AWS, Azure, Docker, Kubernetes, Terraform, CI/CD pipelines and Quantum Computing
> Background in Molecular Engineering 


[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/tu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/adrianalola)
