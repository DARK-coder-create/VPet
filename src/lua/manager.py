from typing import Dict, Any, List, Optional
from src.core.logger import logger
from src.resource.models.resources import ModelResources


class LuaManager:
    def __init__(self, resources: ModelResources):
        self.logger = logger
        self.resources = resources
        self.scripts: Dict[str, Dict[str, Any]] = {}
        self._load_all_scripts()

    def _load_all_scripts(self):
        for content_pack_id, content_pack in self.resources.content_packs.items():
            if hasattr(content_pack, 'scripts'):
                for script_id, script_data in content_pack.scripts.items():
                    full_id = f"{content_pack_id}.{script_id}"
                    self.scripts[full_id] = script_data
                    self.logger.debug(f"Registered script: {full_id}")

    def execute_function(self, script_id: str, function_name: str, *args) -> Any:
        script_data = self.scripts.get(script_id)
        if not script_data:
            self.logger.error(f"Script not found: {script_id}")
            return None

        try:
            lua_func = script_data['runtime'].globals()[function_name]
            if lua_func:
                result = lua_func(*args)
                self.logger.trace(f"Executed {script_id}.{function_name}")
                return result
            else:
                self.logger.warning(f"Function {function_name} not found in {script_id}")
        except Exception as e:
            self.logger.error(f"Error executing {script_id}.{function_name}: {str(e)}")

        return None

    def get_available_functions(self, script_id: str) -> List[str]:
        script_data = self.scripts.get(script_id)
        if not script_data:
            return []

        functions = []
        runtime = script_data['runtime']
        for key in runtime.globals().keys():
            if callable(runtime.globals()[key]):
                functions.append(key)

        return functions

    def execute_all(self, function_name: str, *args) -> None:
        for script_id in list(self.scripts.keys()):
            if function_name in self.get_available_functions(script_id):
                try:
                    self.execute_function(script_id, function_name, *args)
                except Exception as e:
                    logger.error(f"Error executing {function_name} in {script_id}: {str(e)}")