import os
import logging
from datetime import datetime


# Project root = directory containing the "roundup" package
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir = os.path.join(PROJECT_ROOT, "logs")

os.makedirs(log_dir, exist_ok=True)

logs_path = os.path.join(log_dir, LOG_FILE)


logging.basicConfig(
    filename=logs_path,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)