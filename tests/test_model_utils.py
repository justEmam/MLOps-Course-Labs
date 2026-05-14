import pandas as pd


class DummyModel:
    def predict(self, X):
        return [1]

    def predict_proba(self, X):
        import numpy as np

        return np.array([[0.2, 0.8]])


class DummyPreprocessor:
    def transform(self, df: pd.DataFrame):
        return df.values


def test_predict_churn_function(monkeypatch):
    import app.model_utils as mu

    monkeypatch.setattr(mu, "model", DummyModel())
    monkeypatch.setattr(mu, "preprocessor", DummyPreprocessor())

    sample = mu.sample_features()
    res = mu.predict_churn(sample)
    assert isinstance(res, dict)
    assert res["prediction"] in (0, 1)
    assert 0.0 <= res["probability"] <= 1.0


def test_predict_churn_raises_when_no_model(monkeypatch):
    import app.model_utils as mu

    monkeypatch.setattr(mu, "model", None)
    try:
        mu.predict_churn(mu.sample_features())
        assert False, "Expected RuntimeError when model is None"
    except RuntimeError:
        pass
