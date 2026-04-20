# 🚀 MLOps Portfolio Project

An end-to-end MLOps pipeline built with AWS, Docker, Terraform, and GitHub Actions.
Demonstrates production-grade ML infrastructure for a breast cancer classification model.

---

## 🏗️ Architecture

\`\`\`
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
\`\`\`

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

\`\`\`
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
\`\`\`

---

## 🚀 Quick Start

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/adrianalola/mlops-portfolio.git
cd mlops-portfolio
\`\`\`

### 2. Create virtual environment
\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

### 3. Train the model
\`\`\`bash
python app/train.py
\`\`\`

### 4. View experiment tracking
\`\`\`bash
mlflow ui --port 5001
# Open http://127.0.0.1:5001
\`\`\`

### 5. Run the API locally
\`\`\`bash
uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000/docs
\`\`\`

### 6. Run with Docker
\`\`\`bash
docker build -t mlops-cancer-api .
docker run -p 8000:8000 mlops-cancer-api
\`\`\`

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | \`/health\` | Health check — model status |
| GET | \`/info\` | Model metadata and features |
| POST | \`/predict\` | Run inference |

### Example prediction request
\`\`\`bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776,
                 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053,
                 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587,
                 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0,
                 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
  }'
\`\`\`

### Example response
\`\`\`json
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
\`\`\`

---

## ☁️ AWS Infrastructure

Provisioned with Terraform:

- **EC2** (t2.micro) — hosts the Docker container
- **S3 Bucket** — stores trained model artifacts
- **IAM Role** — least privilege access (S3 read-only)
- **Security Group** — allows port 8000 (API) and 22 (SSH)

### Deploy infrastructure
\`\`\`bash
cd infrastructure
terraform init
terraform apply
\`\`\`

### Destroy infrastructure (to avoid costs)
\`\`\`bash
terraform destroy
\`\`\`

---

## 🔄 CI/CD Pipeline

Every push to \`main\` automatically:
1. Connects to EC2 via SSH
2. Pulls latest code from GitHub
3. Downloads model artifacts from S3
4. Builds Docker image
5. Restarts container with zero downtime

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

---

## 👩‍💻 Author

**Adriana** — Cloud & DevOps Engineer transitioning into MLOps

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/tu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/adrianalola)
