from src.resource.models.content_pack import ModelContentPack, ModelErrorContentPack
from typing import List, Dict, AnyStr
from pydantic import BaseModel, Field

class ModelResources(BaseModel):
    content_packs: Dict[AnyStr, ModelContentPack] = Field(default_factory=dict) # noqa
    error_content_packs: List[ModelErrorContentPack] = Field(default_factory=list) # noqa

    @property
    def number_error_load_content_packs(self) -> int:
        return len(self.error_content_packs)