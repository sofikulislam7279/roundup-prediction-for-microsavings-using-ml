from dataclasses import dataclass
from typing import Optional


@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str 
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class RegressionMetricArtifact:
    rmse: float
    mae: float
    r2_score: float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    metric_artifact: RegressionMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    trained_model_rmse: float
    best_model_rmse: float
    hf_model_path: str
    trained_model_path: str


@dataclass
class ModelPusherArtifact:
    bucket_name: str
    hf_model_path: str


@dataclass
class ProductionModel:
    model: object
    rmse: float
    mae: float
    r2_score: float