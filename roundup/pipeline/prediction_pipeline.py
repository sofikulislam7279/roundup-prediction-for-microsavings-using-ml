import sys
from datetime import datetime

import numpy as np
from pandas import DataFrame

from roundup.entity.config_entity import RoundupPredictorConfig
from roundup.entity.hf_estimator import RoundupEstimator
from roundup.exception import RoundupException
from roundup.logger import logging


class RoundupData:
    """
    Prepare transaction data and derived features for roundup prediction.
    """

    def __init__(
        self,
        txn_amount: float,
        category: str,
        txn_count_today: int,
        daily_total_spent: float,
        txn_count_prev_7d: int,
        avg_spend_last_7days: float,
        income_tier: str,
        user_tenure_days: int,
        monthly_savings_so_far: float,
        user_savings_streak: int,
        days_since_last_txn: int,
    ):
        try:
            self.txn_amount = txn_amount
            self.category = category

            self.transaction_time = datetime.now()

            self.txn_count_today = txn_count_today
            self.daily_total_spent = daily_total_spent

            self.txn_count_prev_7d = txn_count_prev_7d
            self.avg_spend_last_7days = avg_spend_last_7days

            self.income_tier = income_tier
            self.user_tenure_days = user_tenure_days

            self.monthly_savings_so_far = monthly_savings_so_far
            self.user_savings_streak = user_savings_streak

            self.days_since_last_txn = days_since_last_txn

        except Exception as e:
            raise RoundupException(e, sys) from e

    def get_roundup_data_as_dict(self) -> dict:
        """
        Create model input features from transaction data.
        """

        logging.info(
            "Entered get_roundup_data_as_dict method"
        )

        try:
            transaction_hour = self.transaction_time.hour

            is_weekend = (
                1
                if self.transaction_time.weekday() >= 5
                else 0
            )

            hour_sin = np.sin(
                2 * np.pi * transaction_hour / 24
            )

            hour_cos = np.cos(
                2 * np.pi * transaction_hour / 24
            )

            remaining_daily_capacity = max(
                0,
                self.avg_spend_last_7days
                - self.daily_total_spent,
            )

            spending_velocity_ratio = (
                self.txn_count_today
                / self.txn_count_prev_7d
                if self.txn_count_prev_7d > 0
                else 0
            )

            pressure_score = (
                self.daily_total_spent
                / self.avg_spend_last_7days
                if self.avg_spend_last_7days > 0
                else 0
            )

            is_new_user = (
                1
                if self.user_tenure_days <= 30
                else 0
            )

            input_data = {
                "txn_amount": [self.txn_amount],
                "category": [self.category],
                "transaction_hour": [transaction_hour],
                "is_weekend": [is_weekend],
                "hour_sin": [hour_sin],
                "hour_cos": [hour_cos],
                "txn_count_today": [self.txn_count_today],
                "daily_total_spent": [self.daily_total_spent],
                "remaining_daily_capacity": [
                    remaining_daily_capacity
                ],
                "txn_count_prev_7d": [
                    self.txn_count_prev_7d
                ],
                "avg_spend_last_7days": [
                    self.avg_spend_last_7days
                ],
                "spending_velocity_ratio": [
                    spending_velocity_ratio
                ],
                "income_tier": [self.income_tier],
                "user_tenure_days": [
                    self.user_tenure_days
                ],
                "is_new_user": [is_new_user],
                "pressure_score": [pressure_score],
                "monthly_savings_so_far": [
                    self.monthly_savings_so_far
                ],
                "user_savings_streak": [
                    self.user_savings_streak
                ],
                "days_since_last_txn": [
                    self.days_since_last_txn
                ],
            }

            logging.info(
                "Created roundup prediction input dictionary"
            )

            return input_data

        except Exception as e:
            raise RoundupException(e, sys) from e

    def get_roundup_input_data_frame(self) -> DataFrame:
        """
        Convert roundup prediction input into a DataFrame.
        """

        try:
            roundup_input_dict = (
                self.get_roundup_data_as_dict()
            )

            dataframe = DataFrame(
                roundup_input_dict
            )

            logging.info(
                f"Created prediction dataframe "
                f"with shape: {dataframe.shape}"
            )

            return dataframe

        except Exception as e:
            raise RoundupException(e, sys) from e


class RoundupPredictor:
    """
    Load the production model and generate roundup predictions.
    """

    def __init__(
        self,
        prediction_pipeline_config: RoundupPredictorConfig | None = None,
    ) -> None:

        try:
            if prediction_pipeline_config is None:
                prediction_pipeline_config = (
                    RoundupPredictorConfig()
                )

            self.prediction_pipeline_config = (
                prediction_pipeline_config
            )

            self.model = RoundupEstimator(
                bucket_name=(
                    prediction_pipeline_config.bucket_name
                ),
                model_path=(
                    prediction_pipeline_config.hf_model_path
                ),
            )

            logging.info(
                "Roundup model loaded successfully"
            )

        except Exception as e:
            raise RoundupException(e, sys) from e

    def predict(
        self,
        txn_amount: float,
        category: str,
        txn_count_today: int,
        daily_total_spent: float,
        txn_count_prev_7d: int,
        avg_spend_last_7days: float,
        income_tier: str,
        user_tenure_days: int,
        monthly_savings_so_far: float,
        user_savings_streak: int,
        days_since_last_txn: int,
    ) -> float:
        """
        Generate a roundup amount prediction.
        """

        logging.info(
            "Entered predict method of RoundupPredictor"
        )

        try:
            roundup_data = RoundupData(
                txn_amount=txn_amount,
                category=category,
                txn_count_today=txn_count_today,
                daily_total_spent=daily_total_spent,
                txn_count_prev_7d=txn_count_prev_7d,
                avg_spend_last_7days=avg_spend_last_7days,
                income_tier=income_tier,
                user_tenure_days=user_tenure_days,
                monthly_savings_so_far=(
                    monthly_savings_so_far
                ),
                user_savings_streak=(
                    user_savings_streak
                ),
                days_since_last_txn=(
                    days_since_last_txn
                ),
            )

            dataframe = (
                roundup_data
                .get_roundup_input_data_frame()
            )

            logging.info(
                f"Prediction dataframe created "
                f"with shape: {dataframe.shape}"
            )

            result = self.model.predict(
                dataframe
            )

            prediction = float(
                result[0]
            )

            logging.info(
                f"Roundup prediction generated: {prediction}"
            )

            return prediction

        except Exception as e:
            raise RoundupException(e, sys) from e