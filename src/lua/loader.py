from lupa import LuaRuntime
from pathlib import Path
from typing import Optional, Dict, Any, List
from src.core.logger import logger
from src.core.models.m_settings import ModelSettings
from src.lua.modules import LUA_FUNCTIONS, LUA_CLASSES

class LoaderLua:
    def __init__(self, config: Optional[ModelSettings] = None):
        self.logger = logger
        self.config = config
        if config is None:
            from src.core.settings import settings
            self.config = settings

    def _create_safe_lua_runtime(self, content_pack_path: Path) -> LuaRuntime:
        try:
            lua = LuaRuntime()
            lua.execute('''
                print = nil
                os = nil
                io = nil
                package = nil
                loadfile = nil
                dofile = nil
            ''')

            def safe_require(modname):
                if not isinstance(modname, str):
                    raise Exception("Module name must be string")
                modpath = modname.replace('.', '/')
                full_path = content_pack_path / f"{modpath}.lua"
                if not (self._is_safe_path(full_path, content_pack_path)):
                    raise Exception(f"Access outside content pack not allowed: {modname}")
                if full_path.exists():
                    file_path = full_path
                else:
                    raise Exception(f"Module not found: {modname}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        module_code = f.read()
                    module_env = lua.table()
                    lua.execute(module_code, module_env)
                    return module_env
                except Exception as e:
                    raise Exception(f"Failed to load module {modname}: {str(e)}")

            lua.globals().require = safe_require
            self._enhance_runtime(lua)
            return lua
        except ImportError as e:
            self.logger.error(f"Failed to create Lua runtime: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error creating Lua runtime: {str(e)}")
            raise

    def _enhance_runtime(self, runtime: LuaRuntime, script_id: str = 'unknown'):
        runtime.globals().script_id = script_id
        for name, fn in LUA_FUNCTIONS.items():
            def wrapper(*args, **kwargs):
                try:
                    line = runtime.eval('debug.getinfo(3).currentline')
                except:
                    line = 'unknown'
                self.logger.info(f"Called <{name}> from <{script_id}> at line <{line}>")
                return fn(*args, **kwargs)
            runtime.globals()[name] = wrapper

        for name, cls in LUA_CLASSES.items():
            wrapped_methods = {}
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name)
                if callable(attr) and not attr_name.startswith('__'):
                    def method_wrapper(self, *args, **kwargs):
                        try:
                            line = runtime.eval('debug.getinfo(3).currentline')
                        except:
                            line = 'unknown'
                        self.logger.debug(f"Called {cls.__name__}.{attr_name} from {script_id} at line {line}")
                        return attr(self, *args, **kwargs)
                    wrapped_methods[attr_name] = method_wrapper
            wrapped_cls = type('Wrapped' + cls.__name__, (cls,), wrapped_methods)
            runtime.globals()[name] = wrapped_cls

    def _is_safe_path(self, target_path: Path, base_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(base_path.resolve())
            return True
        except ValueError:
            return False

    def scan_content_pack_scripts(self, content_pack_path: Path) -> Dict[str, Any]:
        self.logger.info(f"Scanning Lua scripts in: {content_pack_path}")
        scripts = {}

        for lua_file in content_pack_path.rglob("*.lua"):
            if self._is_safe_path(lua_file, content_pack_path):
                script_data = self._load_lua_script(lua_file, content_pack_path)
                if script_data:
                    script_id = lua_file.relative_to(content_pack_path).with_suffix('').as_posix().replace('/', '.')
                    scripts[script_id] = script_data
                    self.logger.info(f"Loaded Lua script: {script_id}")
            else:
                self.logger.warning(f"Unsafe script path: {lua_file}")

        return scripts

    def _load_lua_script(self, script_path: Path, content_pack_path: Path) -> Optional[Dict[str, Any]]:
        try:
            lua_runtime = self._create_safe_lua_runtime(content_pack_path)
            script_id = script_path.relative_to(content_pack_path).with_suffix('').as_posix().replace('/', '.')
            self._enhance_runtime(lua_runtime, script_id)

            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()

            lua_runtime.execute(script_content)

            return {
                'path': script_path,
                'content': script_content,
                'runtime': lua_runtime
            }
        except Exception as e:
            self.logger.error(f"Failed to load Lua script {script_path}: {str(e)}")
            return None