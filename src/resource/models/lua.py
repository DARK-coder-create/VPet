from pathlib import Path
from typing import AnyStr, Optional

from pydantic import BaseModel


class ModelLua(BaseModel):
    path: Path
    raw: AnyStr

    content_pack_id: Optional[AnyStr]