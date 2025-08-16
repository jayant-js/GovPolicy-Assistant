from config.logging_config import setup_logging
import logging

setup_logging()

def get_logger(name):
    return logging.getLogger(name)  