import logging
from logging import NullHandler

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Capture all log levels

# Create file handler
file_handler = logging.FileHandler("logs/etl.log")
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
