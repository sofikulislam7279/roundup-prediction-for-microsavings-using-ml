import sys

from roundup.entity.artifact_entity import (
    ModelEvaluationArtifact,
    ModelPusherArtifact
)

from roundup.entity.config_entity import ModelPusherConfig
from roundup.entity.hf_estimator import RoundupEstimator
from roundup.exception import RoundupException
from roundup.logger import logging



class ModelPusher:

    def __init__(
        self,
        model_pusher_config: ModelPusherConfig
    ):
        try:
            self.model_pusher_config = (
                model_pusher_config
            )

        except Exception as e:
            raise RoundupException(e, sys) from e


    def initiate_model_pusher(
        self,
        model_evaluation_artifact: ModelEvaluationArtifact
    ) -> ModelPusherArtifact:

        try:

            logging.info("Entered initiate_model_pusher method")

            if not model_evaluation_artifact.is_model_accepted:

                logging.info(
                    "Model was not accepted. "
                    "Skipping model upload."
                )

                return ModelPusherArtifact(
                    bucket_name=(
                        self.model_pusher_config
                        .bucket_name
                    ),
                    hf_model_path=""
                )

            estimator = RoundupEstimator(
                bucket_name=(
                    self.model_pusher_config
                    .bucket_name
                ),
                model_path=(
                    self.model_pusher_config
                    .hf_model_path
                )
            )

            estimator.save_model(
                from_file=(
                    model_evaluation_artifact
                    .trained_model_path
                )
            )

            logging.info(
                "Model successfully uploaded "
                "to Hugging Face Bucket."
            )

            model_pusher_artifact = (
                ModelPusherArtifact(
                    bucket_name=(
                        self.model_pusher_config
                        .bucket_name
                    ),
                    hf_model_path=(
                        self.model_pusher_config
                        .hf_model_path
                    )
                )
            )

            return model_pusher_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e