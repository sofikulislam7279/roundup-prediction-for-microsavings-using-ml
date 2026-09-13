import sys
import importlib
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from roundup.exception import RoundupException
from roundup.logger import logging
from roundup.entity.artifact_entity import RegressionMetricArtifact

def import_class(module_name: str, class_name: str) -> object:
    """Dynamically imports a class from a module."""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except Exception as e:
        raise RoundupException(e, sys) from e

def evaluate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> RegressionMetricArtifact:
    """Calculates regression metrics and returns metric artifact."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    return RegressionMetricArtifact(rmse=rmse, mae=mae, r2_score=r2)

def evaluate_models(
    x_train: np.ndarray,
    y_train: np.ndarray,
    model_selection_config: dict,
    randomized_search_config: dict
) -> tuple[object, str, float]:
    """
    Iterates through configured models, performs CV or RandomizedSearchCV, 
    and selects the best model based on RMSE.
    """
    try:
        randomized_search_class = import_class(
            randomized_search_config["module"],
            randomized_search_config["class"]
        )
        randomized_search_params = randomized_search_config.get("params", {})

        best_model = None
        best_model_name = None
        best_cv_rmse = float("inf")

        for model_name, config in model_selection_config.items():
            logging.info(f"Training model: {model_name}")
            
            model_class = import_class(config["module"], config["class"])
            model_params = config.get("params", {})
            search_distributions = config.get("search_param_distributions", {})
            model = model_class(**model_params)

            if not search_distributions:
                cv_scores = cross_val_score(
                    model,
                    x_train,
                    y_train,
                    cv=randomized_search_params.get("cv", 5),
                    scoring="neg_root_mean_squared_error",
                    n_jobs=randomized_search_params.get("n_jobs", -1)
                )
                cv_rmse = -np.mean(cv_scores)
                model.fit(x_train, y_train)
                current_model = model
            else:
                randomized_search = randomized_search_class(
                    estimator=model,
                    param_distributions=search_distributions,
                    **randomized_search_params
                )
                randomized_search.fit(x_train, y_train)
                current_model = randomized_search.best_estimator_
                cv_rmse = -randomized_search.best_score_
                logging.info(f"{model_name} best parameters: {randomized_search.best_params_}")

            logging.info(f"{model_name} CV RMSE: {cv_rmse}")

            if cv_rmse < best_cv_rmse:
                best_cv_rmse = cv_rmse
                best_model = current_model
                best_model_name = model_name

        if best_model is None:
            raise Exception("No suitable regression model was found.")

        return best_model, best_model_name, best_cv_rmse

    except Exception as e:
        raise RoundupException(e, sys) from e