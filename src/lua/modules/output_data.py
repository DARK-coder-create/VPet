from src.core.logger import logger
from . import lua_func

@lua_func(name='print')
def lua_print(*args):
    logger.info(" ".join(args))