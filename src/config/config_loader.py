import yaml
from pathlib import Path

CONFIG_PATH = Path("/app/config.yaml")
def load_config(path: Path = CONFIG_PATH):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config