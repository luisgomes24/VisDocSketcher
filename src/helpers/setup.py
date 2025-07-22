import getpass
import os
from dotenv import load_dotenv
import logging
import sys
from pathlib import Path
from datetime import datetime

load_dotenv(".env")


def _set_env(var: str):
    if not os.environ.get(var):
        if os.getenv(var):
            os.environ[var] = os.getenv(var)
        else:
            os.environ[var] = getpass.getpass(f"{var}: ")


def init_keys():
    print("Initializing keys...")
    _set_env("OPENAI_API_KEY")
    _set_env("TAVILY_API_KEY")


# Configure logging
def setup_logging():
    """Set up logging to both console and file with timestamp."""
    # Create logs directory if it doesn't exist
    logs_dir = "../logs"
    Path(logs_dir).mkdir(exist_ok=True)

    # Create a timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(logs_dir) / f"sketch_creator_{timestamp}.log"

    # Clear any existing handlers
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set up file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

    logger.info(f"Logging to {log_file}")
    return logger
