from typing import Dict
from .base_model import BaseModel


class SessionInfo(BaseModel):
    collection: str | None = "connections"

    def __init__(
        self,
        uuid: str | None = None,
        username: str = None,
        scope: list[str] = None,
        userInfo: Dict[str, str] = None,
        expiration: float = None,
        **kwargs
    ):
        super().__init__(uuid)
        self.username = username
        self.scope = scope
        self.userInfo = userInfo
        self.expiration = expiration
