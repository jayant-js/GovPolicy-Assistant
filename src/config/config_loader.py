import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent

def load_config(path: str = '../config.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config