import importlib
import inspect
import pkgutil
from pathlib import Path
from src.core.logger import logger
from typing import Optional


def lua_func(name: Optional[str] = None):
    def decorator(fn):
        setattr(fn, "__lua_func__", name or fn.__name__)
        return fn
    return decorator

def lua_cls(name: Optional[str] = None):
    def decorator(cls):
        setattr(cls, "__lua_cls__", name or cls.__name__)
        return cls
    return decorator


LUA_FUNCTIONS = {}
LUA_CLASSES = {}

def _discover_lua_components():
    logger.info("Start discovering lua components")
    package_path = Path(__file__).parent
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
        if module_name == '__init__':
            continue

        try:
            module = importlib.import_module(f'.{module_name}', package_name)

            for name, obj in inspect.getmembers(module):
                if hasattr(obj, '__lua_func__'):
                    lua_name = getattr(obj, '__lua_func__')
                    if lua_name in LUA_FUNCTIONS:
                        logger.critical(f"Duplicate lua function {lua_name}")
                        raise Exception(f"Duplicate lua function {lua_name}")
                    LUA_FUNCTIONS[lua_name] = obj
                    logger.info(f"Registered lua function: {lua_name}")

                if hasattr(obj, '__lua_cls__'):
                    lua_name = getattr(obj, '__lua_cls__')
                    if lua_name in LUA_CLASSES:
                        logger.critical(f"Duplicate lua class {lua_name}")
                        raise Exception(f"Duplicate lua class {lua_name}")
                    LUA_CLASSES[lua_name] = obj
                    logger.info(f"Registered lua class: {lua_name}")

        except ImportError as e:
            logger.error(f"Could not import module {module_name}: {e}")

    logger.info("Finished discovering lua components")
    logger.info(f"Loaded functions: {len(LUA_FUNCTIONS)}")
    logger.info(f"Loaded classes: {len(LUA_CLASSES)}")

_discover_lua_components()