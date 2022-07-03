from pydantic import BaseModel

class SearchResultModel(BaseModel):
    title: str
    subtitle: str
    description: str
    image: str
    type: str
    reference: int | str
    canDownload: bool
    canExpand: bool
    similarity: float

__all__ = ["SearchResultModel"]