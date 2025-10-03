from src.core.logger import logger

from functools import wraps
from pathlib import Path
from typing import Optional, Any

import yaml
import json


def handle_file_errors(func):
    @wraps(func)
    def wrapper(path: Path, *args, **kwargs) -> Optional[Any]:
        try:
            return func(path, *args, **kwargs)
        except FileNotFoundError:
            logger.error(f"File not found: {path}")
        except PermissionError:
            logger.error(f"Permission denied for file: {path}")
        except IsADirectoryError:
            logger.error(f"Path is a directory, not a file: {path}")
        except UnicodeDecodeError as e:
            logger.error(f"File decoding error {path}: {e}")
        except yaml.YAMLError as e:
            logger.error(f"YAML syntax error in file {path}: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON syntax error in file {path}: {e}")
        except Exception as e:
            logger.error(f"Unknown error while loading {path}: {e}")
        return None
    return wrapper