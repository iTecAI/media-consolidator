from typing import Any
import pymongo.database
from starlite.datastructures import State
import typing
from keycloak import Keycloak
from .podcast_index import Index

class ApplicationState(State):
    def __init__(self, state: typing.Optional[typing.Dict[str, typing.Any]] = None):
        super().__init__(state)
        self.config: Any = None
        self.database: pymongo.database.Database = None
        self.keycloak: Keycloak = None
        self.podcastIndex: Index = None