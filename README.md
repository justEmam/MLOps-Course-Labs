# Bank Customer Churn Prediction

This repository contains a small ML project that demonstrates training, serving, and deploying a churn prediction model for bank customers. It includes preprocessing, model utilities, a FastAPI server, and CI/CD workflow to build and deploy a Docker image.

## Contents
- **app/**: application code (logger, model utils)
- **src/**: training scripts
- **dataset/**: example CSV data
- **tests/**: unit tests for the API and model utilities
- **.github/workflows/actions.yml**: CI/CD workflow (tests, build, push, deploy)

## Quickstart
Prerequisites: Python 3.12, pip, Docker (optional)

1. Create and activate a virtual environment (optional):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-app.txt
```

2. Run the FastAPI app locally:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

4. Example predict (use the sample JSON in `tests/test_main.py` as payload).

## Docker
Build and run the container:

```powershell
docker build -t churn-api:latest .
docker run --rm -p 8000:8000 --env-file .env -v ${PWD}/mlruns:/app/mlruns churn-api:latest
```

Note: mount your `mlruns/` directory and provide runtime variables in an `.env` on the host. See `.env` template in the repo.

## Tests
Run unit tests with:

```powershell
- [MLflow Integration](#mlflow-integration)
- [Usage](#usage)
```

## CI/CD
The repository contains a GitHub Actions workflow at `.github/workflows/actions.yml` that runs tests, builds and pushes a Docker image (Docker Hub or ECR), and optionally deploys to an EC2 instance when deployment secrets are configured.

## Notes
- `app/model_utils.py` reads `BEST_MODEL_URI` and `BEST_PREPROCESSOR_URI` from environment variables (or `.env` when `python-dotenv` is installed). By default model loading is disabled unless URIs are provided.
- Keep secrets out of the repository. Use GitHub Secrets for CI and host-side `.env` for runtime values on the EC2 host.

If you'd like, I can add a `docker-compose.yml` for local testing or a `workflow_dispatch` trigger for manual runs.

- [Metrics Logged](#metrics-logged)
- [Artifacts](#artifacts)
- [Requirements](#requirements)

---

## Project Overview
This Python module preprocesses customer data, balances the classes, trains multiple machine learning models, evaluates them, and logs all experiments to MLflow. The models are trained to predict whether a customer will exit (churn) or stay with the bank.

---

## Dataset
The dataset is assumed to be in `dataset/Churn_Modelling.csv` and contains customer information such as:

- `CreditScore`
- `Geography`
- `Gender`
- `Age`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`
- `Exited` (target variable: 1 = churn, 0 = stay)

---

## Features
The following features are used for modeling:

**Numerical features:**
- CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary  

**Categorical features:**
- Geography, Gender  

---

## Models
The project trains three models:

1. **Logistic Regression**
2. **Random Forest Classifier**
3. **Support Vector Machine (SVM)**

Each model is trained, evaluated, and logged with MLflow including metrics, parameters, and artifacts.

---

## Preprocessing
The preprocessing pipeline includes:

- Balancing classes via **downsampling** of the majority class
- Splitting data into training and test sets (70%-30%)
- Scaling numerical features with `StandardScaler`
- One-hot encoding categorical features (`Geography` and `Gender`)
- Logging the preprocessor pipeline to MLflow as an artifact

---

## MLflow Integration
All experiments are tracked with MLflow:

- **Tracking URI:** `file:./mlruns`
- **Experiment name:** `churn_prediction`
- **Logged artifacts:**
  - Preprocessing pipeline
  - Trained models
  - Training datasets
  - Confusion matrices (PNG images)
- **Logged parameters:** e.g., `max_iter` for logistic regression
- **Logged metrics:** Accuracy, F1-score, Precision, Recall
- **Logged tags:** Problem type for each model (binary classification)

---

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt

testtesttesttttt