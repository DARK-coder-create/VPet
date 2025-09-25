from pathlib import Path

from pydantic import BaseModel
from typing import Optional, AnyStr, List


class ModelEntity(BaseModel):
    id: AnyStr
    name: Optional[AnyStr] = None
    icon: Optional[AnyStr] = None
    sprite: Optional[AnyStr] = None

    position: Optional[List[AnyStr]] = None
    size: Optional[List[AnyStr]] = None

    scripts: Optional[List[Path]] = None

    content_pack_id: Optional[AnyStr]