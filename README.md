# Bank Customer Churn Prediction

This project demonstrates a machine learning workflow for predicting bank customer churn. It includes preprocessing, model training, evaluation, and experiment tracking using **MLflow**.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Features](#features)
- [Models](#models)
- [Preprocessing](#preprocessing)
- [MLflow Integration](#mlflow-integration)
- [Usage](#usage)
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
