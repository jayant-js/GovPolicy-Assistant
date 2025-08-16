import yaml

def load_config(path: str = '../config.yaml'):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config