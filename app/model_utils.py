import os
from typing import Any, Dict

import pandas as pd

from .logger_setup import get_logger

logger = get_logger("model_utils")

# Load .env if python-dotenv is available (optional). This lets developers
# put local overrides in a .env file during development without requiring
# environment configuration in CI or production.
try:
    from dotenv import load_dotenv

    load_dotenv()
    logger.info("Loaded .env file (if present)")
except Exception:
    # dotenv not installed or .env not present; continue silently
    pass

# Prefer environment variables; default to None so code won't try to load
# large model artefacts unless the user explicitly configures them.
BEST_MODEL_URI = os.environ.get("BEST_MODEL_URI") or None
BEST_PREPROCESSOR_URI = os.environ.get("BEST_PREPROCESSOR_URI") or None


def _try_load_mlflow_model(uri: str):
    if not uri:
        return None

    try:
        import mlflow.sklearn
        # Try mlflow loader first (accepts model directory or URI)
        try:
            return mlflow.sklearn.load_model(uri)
        except Exception:
            # Fallback: if a raw pickle/joblib file is provided, try joblib
            if str(uri).lower().endswith(".pkl") or str(uri).lower().endswith(".joblib"):
                try:
                    import joblib

                    # strip file:// prefix if present
                    path = uri.replace("file://", "")
                    return joblib.load(path)
                except Exception:
                    raise
            raise
    except Exception as e:  # pragma: no cover - environment-dependent
        logger.info("mlflow model load failed for %s: %s", uri, e)
        return None


# Load at module import time so the API can serve immediately when URIs are
# explicitly provided. If URIs are not set, the model and preprocessor stay
# unset (None) and callers/tests can monkeypatch them.
model = None
preprocessor = None
if BEST_MODEL_URI:
    model = _try_load_mlflow_model(BEST_MODEL_URI)
else:
    logger.info("BEST_MODEL_URI not set; model not loaded")

if BEST_PREPROCESSOR_URI:
    preprocessor = _try_load_mlflow_model(BEST_PREPROCESSOR_URI)
else:
    logger.info("BEST_PREPROCESSOR_URI not set; preprocessor not loaded")


def sample_features() -> Dict[str, Any]:
    """Return a sample feature dict matching training features.

    Follow the same feature names used in preprocessing/training.
    """
    return {
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


def predict_churn(features: Dict[str, Any]) -> Dict[str, Any]:
    """Predict churn using the loaded model and optional preprocessor.

    Returns a dict with keys: `prediction` (0/1) and `probability` (float|None).
    Raises RuntimeError if model is not loaded.
    """
    if model is None:
        raise RuntimeError("Model not loaded. Set BEST_MODEL_URI or train a model first.")

    df = pd.DataFrame([features])

    if preprocessor is not None:
        try:
            transformed = preprocessor.transform(df)
            # Keep as DataFrame to play nicely with sklearn estimators
            X = pd.DataFrame(transformed)
        except Exception:
            logger.exception("Preprocessor transform failed, passing raw features")
            X = df
    else:
        X = df

    try:
        pred = int(model.predict(X)[0])
    except Exception:
        logger.exception("Model prediction failed")
        raise

    proba = None
    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba(X)
            # probs expected shape: (n_samples, n_classes)
            try:
                proba = float(probs[0][1])
            except Exception:
                # if single-column or different layout, try other accesses
                import numpy as _np

                arr = _np.asarray(probs)
                if arr.ndim == 1:
                    proba = float(arr[0])
                else:
                    proba = float(arr[0, -1])
        except Exception:
            logger.exception("predict_proba failed")
            proba = None

    result = {"prediction": pred, "probability": proba}
    logger.info("Prediction result: %s", result)
    return result


if __name__ == "__main__":
    # quick manual check
    logger.info("Sample predict: %s", predict_churn(sample_features()))
