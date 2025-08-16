import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger("gov-policy-rag")