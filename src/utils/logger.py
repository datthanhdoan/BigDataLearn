# src/utils/logger.py
from config.logging_config import setup_logger

# Create loggers for different components
producer_logger = setup_logger('producer')
consumer_logger = setup_logger('consumer')