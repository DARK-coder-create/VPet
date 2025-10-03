from pydantic import BaseModel, Field
from typing import AnyStr, List, SupportsInt


class ModelSettings(BaseModel):
    version: AnyStr = "unknown"

    content_packs_dirs: List[AnyStr] = Field(default=["data/content_packs"]) # noqa
    save_directory: List[AnyStr] = Field(default=["data/saves"]) # noqa

    log_directory: AnyStr = "data/logs"

    file_name_for_content_pack: AnyStr = "info"

    global_timer_tick: int = 24
