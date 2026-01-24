"""
Configuration module for Sales Data Pipeline
Handles environment variables and database configuration
"""
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sales_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

def setup_logging(log_file='sales_pipeline.log'):
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
    """
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
