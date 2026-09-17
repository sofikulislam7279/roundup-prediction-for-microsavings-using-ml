import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from roundup.exception import RoundupException
from roundup.logger import logging
from roundup.pipeline.prediction_pipeline import RoundupPredictor
from roundup.constants import APP_HOST, APP_PORT


predictor: RoundupPredictor | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load the production model once when FastAPI starts.
    """

    global predictor

    try:
        logging.info("Loading Jomao round-up model...")

        predictor = RoundupPredictor()

        logging.info("Jomao round-up model ready")

        yield

    except Exception as e:
        logging.error(
            f"Failed to load Jomao round-up model: {e}"
        )

        raise

    finally:
        predictor = None

        logging.info("Jomao round-up model unloaded")



app = FastAPI(
    title="Jomao Adaptive Round-up Prediction",
    description=(
        "Machine learning prediction engine for "
        "adaptive micro-savings."
    ),
    version="1.0.0",
    lifespan=lifespan,
)



app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")


class TransactionInput(BaseModel):
    """
    Raw user inputs for round-up prediction.
    """

    txn_amount: float = Field(
        ...,
        gt=0,
        description="Transaction amount in Tk",
    )

    category: str = Field(
        ...,
        min_length=1,
    )

    txn_count_today: int = Field(
        ...,
        ge=0,
    )

    daily_total_spent: float = Field(
        ...,
        ge=0,
    )

    txn_count_prev_7d: int = Field(
        ...,
        ge=0,
    )

    avg_spend_last_7days: float = Field(
        ...,
        ge=0,
    )

    income_tier: str = Field(
        ...,
        min_length=1,
    )

    user_tenure_days: int = Field(
        ...,
        ge=0,
    )

    monthly_savings_so_far: float = Field(
        ...,
        ge=0,
    )

    user_savings_streak: int = Field(
        ...,
        ge=0,
    )

    days_since_last_txn: int = Field(
        ...,
        ge=0,
    )


# ==========================================================
# Routes
# ==========================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render the Jomao ML showcase frontend.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
async def health():
    """
    Basic health check.
    """

    return {
        "status": "healthy",
        "model_loaded": predictor is not None,
    }


@app.post("/predict")
async def predict_roundup(payload: TransactionInput):
    """
    Generate a round-up prediction from the trained model.
    """

    try:
        if predictor is None:
            raise RoundupException(
                RuntimeError("Model is not loaded yet"),
                sys,
            )

        roundup_amount = predictor.predict(
            **payload.model_dump()
        )

        roundup_amount = round(
            max(float(roundup_amount), 0.0),
            2,
        )

        rounded_total = round(
            payload.txn_amount + roundup_amount,
            2,
        )

        logging.info(
            "Round-up prediction generated successfully"
        )

        return JSONResponse(
            {
                "original_amount": round(
                    payload.txn_amount,
                    2,
                ),
                "roundup_amount": roundup_amount,
                "rounded_total": rounded_total,
            }
        )

    except RoundupException as e:
        logging.error(
            f"Round-up prediction failed: {e}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": (
                    "Couldn't calculate a round-up "
                    "for this transaction. "
                    "Check the numbers and try again."
                )
            },
        )

    except Exception as e:
        logging.error(
            f"Unexpected prediction error: {e}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": (
                    "An unexpected error occurred "
                    "while generating the prediction."
                )
            },
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True,
    )