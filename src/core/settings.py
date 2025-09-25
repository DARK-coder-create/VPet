from src.resource.loader import Loader
from src.core.logger import logger
from pydantic import BaseModel, ValidationError
from pydantic import Field
from typing import AnyStr, List
from pathlib import Path
import os


BASE_PATH_SETTINGS = Path("data/settings.yaml")


class ModelSettings(BaseModel):
    content_packs_dirs: List[AnyStr] = Field(default=["data/content_packs"]) # noqa
    save_directory: List[AnyStr] = Field(default=["data/saves"]) # noqa
    log_directory: AnyStr = "data/logs"
    version: AnyStr = "unknown"


class Settings:
    def __init__(self):
        logger.info("Create Settings")
        self._data = self.load_settings(BASE_PATH_SETTINGS)

    @staticmethod
    def load_settings(path: Path) -> ModelSettings:
        logger.info(f"Load settings from {path}")
        if not os.path.exists(path):
            logger.warning(f"Not found {path}")

            data = ModelSettings(**{})
            Settings.save_settings(path, data)
            return data

        try:
            loaded_data = Loader.load_yaml(path)
            if not loaded_data:
                logger.error("File settings is void, set default settings in settings.yaml")
                data = ModelSettings(**{})
                Settings.save_settings(path, data)
                return data
            logger.debug(f"Load settings is successfully {loaded_data}")
            return ModelSettings(**loaded_data)

        except ValidationError as e:
            logger.exception(f"Error load settings for settings: {e}")
            logger.debug("Use default settings")
            return ModelSettings(**{})

    @staticmethod
    def save_settings(path: Path, data: ModelSettings):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        Loader.save_yaml(path, data.model_dump())
        logger.debug(f"Save settings to {path}")

    def update_settings(self, **kwargs):
        try:
            self._data = self._data.model_copy(update=kwargs)
        except ValidationError as e:
            logger.exception(f"Error update settings: {e}")

    def __getattr__(self, item):
        if hasattr(self._data, item):
            return getattr(self._data, item)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __getitem__(self, item):
        return getattr(self._data, item)

    def __repr__(self):
        return f"Settings({self._data.model_dump()})"

    @property
    def data(self) -> ModelSettings:
        return self._data



settings = Settings()