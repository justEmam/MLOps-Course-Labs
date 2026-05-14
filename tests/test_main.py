from fastapi.testclient import TestClient

import app.model_utils as mu
from main import app


class DummyModel:
    def predict(self, X):
        return [0]

    def predict_proba(self, X):
        import numpy as np

        return np.array([[0.6, 0.4]])


def test_health_and_home():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Churn Prediction API" in r.json().get("message", "")

    r2 = client.get("/health")
    assert r2.status_code == 200
    assert r2.json() == {"status": "ok"}


def test_predict_endpoint(monkeypatch):
    client = TestClient(app)

    monkeypatch.setattr(mu, "model", DummyModel())
    monkeypatch.setattr(mu, "preprocessor", None)

    payload = {
        "CreditScore": 650,
        "Geography": "France",
        "Gender": "Male",
        "Age": 40,
        "Tenure": 3,
        "Balance": 60000.0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 50000.0,
    }

    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "result" in body
    assert body["result"]["prediction"] in (0, 1)


def test_predict_invalid_input():
    client = TestClient(app)
    # missing required field -> validation error
    r = client.post("/predict", json={"CreditScore": 123})
    assert r.status_code == 422
