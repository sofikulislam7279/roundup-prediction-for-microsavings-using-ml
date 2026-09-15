import os
import sys

from roundup.cloud_storage.storage_service import HFStorageService
from roundup.exception import RoundupException
from roundup.utils.common_utils import load_object


class RoundupEstimator:

    def __init__(
        self,
        bucket_name: str,
        model_path: str
    ):
        try:
            self.bucket_name = bucket_name
            self.model_path = model_path

            self.hf_storage = HFStorageService()
            self.loaded_model = None

        except Exception as e:
            raise RoundupException(e, sys) from e

    def is_model_present(self) -> bool:
        """
        Check whether a trained model already exists
        in the Hugging Face Bucket.
        """
        try:
            return self.hf_storage.file_exists(
                bucket_name=self.bucket_name,
                hf_filename=self.model_path
            )

        except Exception as e:
            raise RoundupException(e, sys) from e

    def load_model(self):
        """
        Download the production model from
        Hugging Face Bucket and load it locally.
        """
        try:
            local_model_path = os.path.join(
                "artifact",
                "hf_model",
                "model.pkl"
            )

            os.makedirs(
                os.path.dirname(local_model_path),
                exist_ok=True
            )

            self.hf_storage.download_file(
                bucket_name=self.bucket_name,
                hf_filename=self.model_path,
                local_filename=local_model_path
            )

            self.loaded_model = load_object(
                file_path=local_model_path
            )

            return self.loaded_model

        except Exception as e:
            raise RoundupException(e, sys) from e

    def save_model(
        self,
        from_file: str,
        remove: bool = False
    ) -> None:
        """
        Upload the trained model to
        Hugging Face Bucket.
        """
        try:
            self.hf_storage.upload_file(
                from_file=from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )

        except Exception as e:
            raise RoundupException(e, sys) from e

    def predict(self, dataframe):

        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()

            return self.loaded_model.model.predict(dataframe)

        except Exception as e:
            raise RoundupException(e, sys) from e