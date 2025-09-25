from pathlib import Path

from pydantic import BaseModel
from pydantic.v1 import Field
from typing import List, AnyStr, Union


class ModelContentPack(BaseModel):
    id: AnyStr
    title: AnyStr = "unknown"
    version: AnyStr = "unknown"
    description: AnyStr = ""

    icon: Union[Path, None] = None

    dependencies: List[AnyStr] = Field(default_factory=list)

    authors: List[AnyStr] = Field(default_factory=list)

    path: Union[Path, None] = None