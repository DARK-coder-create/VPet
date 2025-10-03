from pathlib import Path

from pydantic import BaseModel, Field
from typing import List, AnyStr, Union, Optional, Dict, Any


class ModelContentPack(BaseModel):
    id: AnyStr
    title: AnyStr = "unknown"
    version: AnyStr = "unknown"
    description: AnyStr = ""

    icon: Union[Path, None] = None

    dependencies: List[AnyStr] = Field(default_factory=list) # noqa

    entities: Dict[str, Any] = Field(default_factory=dict) # noqa
    scripts: Dict[str, Any] = Field(default_factory=dict)  # noqa

    authors: List[AnyStr] = Field(default_factory=list) # noqa

    path: Union[Path, None] = None


class ModelErrorContentPack(BaseModel):
    id: Optional[AnyStr] = None
    error: AnyStr = "unknown"
    path: Union[Path, None] = None