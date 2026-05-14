"""App package exports.

Expose the actual module names and a small set of package-level helpers
so tests and callers can import from `app` directly when useful.
"""
from .logger_setup import get_logger
from .model_utils import predict_churn, sample_features

__all__ = ["get_logger", "predict_churn", "sample_features", "model_utils", "logger_setup"]
