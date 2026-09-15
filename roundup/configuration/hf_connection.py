import os
import sys

from huggingface_hub import HfApi

from roundup.constants import HF_TOKEN_ENV_KEY
from roundup.exception import RoundupException


class HFClient:

    hf_api = None

    def __init__(self):
        try:

            if HFClient.hf_api is None:

                hf_token = os.getenv(
                    HF_TOKEN_ENV_KEY
                )

                if hf_token is None:
                    raise Exception(
                        f"Environment variable "
                        f"{HF_TOKEN_ENV_KEY} is not set."
                    )

                HFClient.hf_api = HfApi(
                    token=hf_token
                )

            self.hf_api = HFClient.hf_api

        except Exception as e:
            raise RoundupException(e, sys) from e