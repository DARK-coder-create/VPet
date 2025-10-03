from src.core.models.m_settings import ModelSettings
from src.lua.loader import LoaderLua
from src.resource.models.content_pack import ModelContentPack, ModelErrorContentPack
from src.resource.models.entity import ModelEntity
from src.resource.models.resources import ModelResources
from src.resource.handlers import handle_file_errors
from src.core.logger import logger

from pathlib import Path
from typing import Optional, Any, Dict, AnyStr, Counter, List
import yaml


class Loader:

    def __init__(self, config: Optional[ModelSettings] = None):
        logger.info("Init Loader")
        self.config = config
        if config is None:
            from src.core.settings import settings
            self.config = settings

    def scan(self, dirs: Optional[Path] = None) -> ModelResources:
        logger.info("Scan dirs: {}".format(dirs))
        if dirs is None:
            dirs = self.config.content_packs_dirs

        resources = ModelResources()
        for _dir in dirs:
            for path in Path(_dir).iterdir():
                if not path.is_dir():
                    continue

                logger.debug(f"Check dir: {path.__str__()}")
                logger.debug("Get raw content pack info")

                content_pack_info = self._load_content_pack_info(path)
                if content_pack_info is None:
                    error_str = f"Dir {path.__str__()}: Raw content pack info not found"
                    resources.error_content_packs.append(ModelErrorContentPack(path=path, error=error_str))
                    logger.error(error_str)
                    continue
                elif content_pack_info.get("id", None) is None or not isinstance(content_pack_info["id"], str):
                    error_str = f"Dir {path.__str__()}: Raw content pack id not found"
                    resources.error_content_packs.append(
                        ModelErrorContentPack(id=content_pack_info.get("id"), path=path, error=error_str))
                    logger.warning(error_str)
                    continue

                logger.info(f"Start loading raw content pack: {path.__str__()}")
                content_pack = ModelContentPack(**content_pack_info)
                content_pack = content_pack.model_copy(update={"path": path})

                # Загрузка entities
                content_pack.entities = self._load_entities_from_content_pack(content_pack)
                # Загрузка Lua скриптов
                content_pack.scripts = self._load_scripts_from_content_pack(content_pack)

                resources.content_packs[content_pack_info["id"]] = content_pack

        return resources

    def _load_scripts_from_content_pack(self, content_pack: ModelContentPack) -> Dict[str, Any]:
        loader_lua = LoaderLua(self.config)
        return loader_lua.scan_content_pack_scripts(content_pack.path)

    def _load_entities_from_content_pack(self, content_pack_info: ModelContentPack) -> Dict[AnyStr, ModelEntity]:
        _temp_id = []
        entities = {}
        for file in content_pack_info.path.rglob("*.yaml"):  # type: Path
            if file.stem == self.config.file_name_for_content_pack:
                continue
            logger.debug(f"File found: {file.__str__()}")

            data = self.load_yaml(file)
            if data is None:
                logger.warning(f"File {file.__str__()}: data not found")
                continue
            elif data.get("id", None) is None:
                logger.warning(f"File {file.__str__()}: id not found")
                continue
            elif data["id"] in _temp_id:
                logger.error(f"File {file.__str__()}: id is already ")
                return {}

            data["content_pack_id"] = content_pack_info.id

            entity = ModelEntity(**data)

            logger.info(f"Entity(id='{data['id']}') found from file {file.__str__()}")
            entities[entity.id] = entity
        return entities if len(entities) > 0 else []

    def _load_content_pack_info(self, path: Path) -> Optional[Dict[str, Any]]:
        info_path = path / f"{self.config.file_name_for_content_pack}.{'yaml'}"
        if info_path.exists():
            return self.load_yaml(info_path)
        logger.warning(f"Not found content pack info: {info_path}")
        return None


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