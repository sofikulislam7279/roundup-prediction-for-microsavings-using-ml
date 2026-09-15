import sys

from roundup.exception import RoundupException
from roundup.logger import logging

from roundup.components.data_ingestion import DataIngestion
from roundup.components.data_validation import DataValidation
from roundup.components.data_transformation import DataTransformation
from roundup.components.model_trainer import ModelTrainer
from roundup.components.model_evaluation import ModelEvaluation
from roundup.components.model_pusher import ModelPusher

from roundup.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)

from roundup.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
)


class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion(
        self
    ) -> DataIngestionArtifact:
        """
        Start the data ingestion component.
        """
        try:
            logging.info(
                "Entered start_data_ingestion method of TrainingPipeline"
            )

            logging.info("Getting the data from MongoDB")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )

            logging.info(
                "Got the train and test data from MongoDB"
            )

            logging.info(
                "Exited start_data_ingestion method of TrainingPipeline"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def start_data_validation(
        self,
        data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        """
        Start the data validation component.
        """
        try:
            logging.info(
                "Entered start_data_validation method of TrainingPipeline"
            )

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            data_validation_artifact = (
                data_validation.initiate_data_validation()
            )

            logging.info("Performed data validation")

            logging.info(
                "Exited start_data_validation method of TrainingPipeline"
            )

            return data_validation_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def start_data_transformation(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        """
        Start the data transformation component.
        """
        try:
            logging.info(
                "Entered start_data_transformation method "
                "of TrainingPipeline"
            )

            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )

            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                "Exited start_data_transformation method "
                "of TrainingPipeline"
            )

            return data_transformation_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def start_model_trainer(
        self,
        data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        """
        Start the model training component.
        """
        try:
            logging.info(
                "Entered start_model_trainer method of TrainingPipeline"
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )

            model_trainer_artifact = (
                model_trainer.initiate_model_trainer()
            )

            logging.info(
                "Exited start_model_trainer method of TrainingPipeline"
            )

            return model_trainer_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def start_model_evaluation(
        self,
        model_trainer_artifact: ModelTrainerArtifact
    ) -> ModelEvaluationArtifact:
        """
        Start the model evaluation component.
        """
        try:
            logging.info(
                "Entered start_model_evaluation method "
                "of TrainingPipeline"
            )

            model_evaluation = ModelEvaluation(
                model_evaluation_config=self.model_evaluation_config
            )

            model_evaluation_artifact = (
                model_evaluation.initiate_model_evaluation(
                    model_trainer_artifact=model_trainer_artifact
                )
            )

            logging.info(
                "Exited start_model_evaluation method "
                "of TrainingPipeline"
            )

            return model_evaluation_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def start_model_pusher(
        self,
        model_evaluation_artifact: ModelEvaluationArtifact
    ) -> ModelPusherArtifact:
        """
        Start the model pusher component.
        """
        try:
            logging.info(
                "Entered start_model_pusher method of TrainingPipeline"
            )

            model_pusher = ModelPusher(
                model_pusher_config=self.model_pusher_config
            )

            model_pusher_artifact = (
                model_pusher.initiate_model_pusher(
                    model_evaluation_artifact=model_evaluation_artifact
                )
            )

            logging.info(
                "Exited start_model_pusher method of TrainingPipeline"
            )

            return model_pusher_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def run_pipeline(self) -> None:
        """
        Run the complete training pipeline.
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )

            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            model_evaluation_artifact = self.start_model_evaluation(
                model_trainer_artifact=model_trainer_artifact
            )

            model_pusher_artifact = self.start_model_pusher(
                model_evaluation_artifact=model_evaluation_artifact
            )

            logging.info(
                f"Model pusher artifact: {model_pusher_artifact}"
            )

        except Exception as e:
            raise RoundupException(e, sys) from e