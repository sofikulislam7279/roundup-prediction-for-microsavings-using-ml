import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from roundup.exception import RoundupException
from roundup.logger import logging

# NOTE: adjust this import to wherever RoundupPredictor actually lives in your
# project layout (the class from the prediction.py you shared).
from roundup.pipeline.prediction_pipeline import RoundupPredictor

predictor: RoundupPredictor | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model once at startup instead of on every request."""
    global predictor
    logging.info("Loading Jomao round-up model...")
    predictor = RoundupPredictor()
    logging.info("Jomao round-up model ready")
    yield
    predictor = None


app = FastAPI(title="Jomao Round-Up Engine", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TransactionInput(BaseModel):
    txn_amount: float = Field(..., gt=0, description="Transaction amount, Tk")
    category: str
    txn_count_today: int = Field(..., ge=0)
    daily_total_spent: float = Field(..., ge=0)
    txn_count_prev_7d: int = Field(..., ge=0)
    avg_spend_last_7days: float = Field(..., ge=0)
    income_tier: str
    user_tenure_days: int = Field(..., ge=0)
    monthly_savings_so_far: float = Field(..., ge=0)
    user_savings_streak: int = Field(..., ge=0)
    days_since_last_txn: int = Field(..., ge=0)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/predict")
async def predict_roundup(payload: TransactionInput):
    """Run one transaction through the model and return the round-up breakdown."""
    try:
        if predictor is None:
            raise RoundupException(
                RuntimeError("Model is not loaded yet"), sys
            )

        roundup_amount = predictor.predict(**payload.model_dump())
        roundup_amount = round(max(roundup_amount, 0.0), 2)
        rounded_total = round(payload.txn_amount + roundup_amount, 2)

        return JSONResponse(
            {
                "original_amount": round(payload.txn_amount, 2),
                "roundup_amount": roundup_amount,
                "rounded_total": rounded_total,
            }
        )

    except RoundupException as e:
        logging.error(f"Round-up prediction failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Couldn't calculate a round-up for this transaction. Check the numbers and try again."
            },
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)