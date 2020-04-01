import logging.config
import os

import yaml

__all__ = [
    'logger'
]


def create_logger(
        default_path: str = 'logging.yaml',
        default_level: int = logging.INFO):
    logging_config = os.getenv('LOGGING_CONFIG', None)
    path = logging_config if logging_config else default_path

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    return logging.getLogger()


logger = create_logger()
