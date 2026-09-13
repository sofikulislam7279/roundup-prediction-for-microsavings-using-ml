import sys
from typing import Tuple
import numpy as np

from roundup.exception import RoundupException
from roundup.logger import logging
from roundup.utils.common_utils import (
    load_numpy_array_data,
    load_object,
    save_object,
    read_yaml_file
)

from roundup.utils.model_utils import (
    evaluate_models,
    evaluate_regression_metrics
)

from roundup.entity.config_entity import ModelTrainerConfig
from roundup.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    RegressionMetricArtifact
)
from roundup.entity.estimator import RoundupModel


class ModelTrainer:

    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig
    ):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise RoundupException(e, sys) from e

    def get_model_object_and_report(
        self,
        train: np.ndarray,
        test: np.ndarray
    ) -> Tuple[object, RegressionMetricArtifact]:
        try:
            logging.info("Entered get_model_object_and_report method")

            model_config = read_yaml_file(file_path=self.model_trainer_config.model_config_file_path)
            
            x_train, y_train = train[:, :-1], train[:, -1]
            x_test, y_test = test[:, :-1], test[:, -1]

            best_model, best_model_name, best_cv_rmse = evaluate_models(
                x_train=x_train,
                y_train=y_train,
                model_selection_config=model_config["model_selection"],
                randomized_search_config=model_config["randomized_search"]
            )

            logging.info(f"Selected best model: {best_model_name} with CV RMSE: {best_cv_rmse}")

            y_pred = best_model.predict(x_test)
            metric_artifact = evaluate_regression_metrics(y_test, y_pred)
            
            logging.info(f"Test Evaluation Metrics: {metric_artifact}")
            return best_model, metric_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method")
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            best_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            roundup_model = RoundupModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=best_model
            )


            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=roundup_model
            )

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )

            logging.info(f"Model trainer artifact created successfully: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise RoundupException(e, sys) from e