import os
import sys

from roundup.cloud_storage.storage_service import HFStorageService

from roundup.entity.artifact_entity import (
    ModelEvaluationArtifact,
    ModelTrainerArtifact
)

from roundup.entity.config_entity import ModelEvaluationConfig
from roundup.exception import RoundupException
from roundup.logger import logging
from roundup.utils.common_utils import load_object

class ModelEvaluation:

    def __init__(
        self,
        model_evaluation_config: ModelEvaluationConfig
    ):
        try:
            self.model_evaluation_config = (
                model_evaluation_config
            )

            self.hf_storage = HFStorageService()

        except Exception as e:
            raise RoundupException(e, sys) from e


    def get_production_model(self):

        try:

            model_exists = self.hf_storage.file_exists(
                bucket_name=(
                    self.model_evaluation_config
                    .bucket_name
                ),
                hf_filename=(
                    self.model_evaluation_config
                    .hf_model_path
                )
            )

            if not model_exists:
                return None

            local_model_path = os.path.join(
                "artifact",
                "hf_model",
                "existing_model.pkl"
            )

            os.makedirs(
                os.path.dirname(local_model_path),
                exist_ok=True
            )

            self.hf_storage.download_file(
                bucket_name=(
                    self.model_evaluation_config
                    .bucket_name
                ),
                hf_filename=(
                    self.model_evaluation_config
                    .hf_model_path
                ),
                local_filename=local_model_path
            )

            production_model = load_object(
                file_path=local_model_path
            )

            return production_model

        except Exception as e:
            raise RoundupException(e, sys) from e


    def initiate_model_evaluation(
        self,
        model_trainer_artifact: ModelTrainerArtifact
    ) -> ModelEvaluationArtifact:

        try:

            # Load newly trained ProductionModel
            trained_model = load_object(
                file_path=(
                    model_trainer_artifact
                    .trained_model_file_path
                )
            )

            trained_model_rmse = trained_model.rmse

            # Load existing production model
            existing_production_model = (
                self.get_production_model()
            )

            # First training run
            if existing_production_model is None:

                best_model_rmse = float("inf")

                is_model_accepted = True

            else:

                best_model_rmse = (
                    existing_production_model.rmse
                )

                is_model_accepted = (
                    trained_model_rmse
                    < best_model_rmse
                )

            logging.info(
                f"Trained model RMSE: "
                f"{trained_model_rmse}"
            )

            logging.info(
                f"Production model RMSE: "
                f"{best_model_rmse}"
            )

            logging.info(
                f"Model accepted: "
                f"{is_model_accepted}"
            )

            model_evaluation_artifact = (
                ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    trained_model_rmse=trained_model_rmse,
                    best_model_rmse=best_model_rmse,
                    hf_model_path=(
                        self.model_evaluation_config
                        .hf_model_path
                    ),
                    trained_model_path=(
                        model_trainer_artifact
                        .trained_model_file_path
                    )
                )
            )

            return model_evaluation_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e