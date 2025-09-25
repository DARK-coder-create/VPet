from src.core.logger import logger
from functools import wraps
from pathlib import Path
from typing import Optional, Any, Dict
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


class Loader:
    def __init__(self):
        pass

    @staticmethod
    @handle_file_errors
    def load_yaml(path: Path) -> Optional[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            logger.debug(f"Load yaml {path.__str__()}")
            return yaml.safe_load(f)

    @staticmethod
    @handle_file_errors
    def save_yaml(path: Path, data: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            logger.debug(f"Save yaml {path.__str__()}")
            f.write(yaml.dump(data, default_flow_style=False))