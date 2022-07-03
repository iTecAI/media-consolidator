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
    canUpdate: bool
    similarity: float
    lastDownload: float | None

__all__ = ["SearchResultModel"]