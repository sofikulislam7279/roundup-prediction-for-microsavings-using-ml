import sys
import pandas as pd
import numpy as np
from roundup.exception import RoundupException
from roundup.logger import logging

class RoundupModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        :param preprocessing_object: The fitted scikit-learn Pipeline (includes drop_columns, scaling, encoding)
        :param trained_model_object: The fitted regressor/estimator object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> np.ndarray:
        """
        Transforms raw input DataFrame through the saved preprocessor pipeline
        and generates predictions from the trained model.
        """
        try:
            logging.info("Starting prediction process with RoundupModel wrapper")
            
            # Preprocessing pipeline drops columns, scales num features, and one-hot encodes cat features
            transformed_feature = self.preprocessing_object.transform(dataframe)
            
            logging.info("Successfully transformed features. Executing model prediction...")
            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise RoundupException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"