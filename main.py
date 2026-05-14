from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.logger_setup import get_logger
from app.model_utils import predict_churn, sample_features

logger = get_logger("api")

# # Optional HyperDX integration (no-op if not installed or API key missing)
# try:
#     import os

#     if os.environ.get("HYPERDX_API_KEY"):
#         try:
#             import hyperdx

#             hyperdx.configure(api_key=os.environ.get("HYPERDX_API_KEY"))
#             logger.info("HyperDX configured")
#         except Exception:
#             logger.info("HyperDX not available or failed to configure")
# except Exception:
#     pass


app = FastAPI(title="Churn Prediction API")


class ChurnRequest(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


@app.get("/")
def home():
    logger.info("Home endpoint called")
    return {"message": "Churn Prediction API", "sample_input": sample_features()}


@app.get("/health")
def health():
    logger.info("Health check")
    return {"status": "ok"}


@app.post("/predict")
def predict(req: ChurnRequest):
    features = req.dict()
    logger.info("/predict called",)
    try:
        result = predict_churn(features)
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))

    return {"input": features, "result": result}
