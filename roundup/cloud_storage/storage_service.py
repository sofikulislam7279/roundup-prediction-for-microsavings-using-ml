import os
import sys

from huggingface_hub import (
    batch_bucket_files,
    download_bucket_files,
    list_bucket_tree,
)

from roundup.configuration.hf_connection import HFClient
from roundup.exception import RoundupException


class HFStorageService:

    def __init__(self):
        try:
            self.hf_client = HFClient()
            self.hf_api = self.hf_client.hf_api

        except Exception as e:
            raise RoundupException(e, sys) from e

    def upload_file(
        self,
        from_file: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = False
    ) -> None:

        try:

            batch_bucket_files(
                bucket_name,
                add=[
                    (
                        from_file,
                        to_filename
                    )
                ]
            )

            if remove:
                os.remove(from_file)

        except Exception as e:
            raise RoundupException(e, sys) from e

    def download_file(
        self,
        bucket_name: str,
        hf_filename: str,
        local_filename: str
    ) -> None:

        try:

            os.makedirs(
                os.path.dirname(local_filename),
                exist_ok=True
            )

            download_bucket_files(
                bucket_name,
                files=[
                    (
                        hf_filename,
                        local_filename
                    )
                ]
            )

        except Exception as e:
            raise RoundupException(e, sys) from e

    def file_exists(
        self,
        bucket_name: str,
        hf_filename: str
    ) -> bool:

        try:

            files = list_bucket_tree(
                bucket_name,
                recursive=True
            )

            for file in files:

                if (
                    file.type == "file"
                    and file.path == hf_filename
                ):
                    return True

            return False

        except Exception as e:
            raise RoundupException(e, sys) from e