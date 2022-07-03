from typing import Any, Dict, List
from starlite import Controller, Provide, get, ValidationException, State
from pydantic import BaseModel
from util import PodcastEpisodeModel, PodcastModel, uuid_dep, guard_loggedIn

class PodcastResponseModel(BaseModel):
    uuid: str | None
    id: int
    title: str
    url: str
    originalUrl: str
    link: str
    description: str
    author: str
    ownerName: str
    image: str
    artwork: str
    contentType: str
    language: str
    categories: Dict[int, str]
    lastScrape: float = 0

class PodcastController(Controller):
    path: str = "/sources/podcasts"
    guards = [guard_loggedIn]
    tags = ["podcasts"]
    dependencies = {"uuid": Provide(uuid_dep)}

    @get(path="/search")
    async def search_podcasts(self, q: str, state: State) -> List[PodcastResponseModel]:
        try:
            results: List[PodcastModel] = state.podcastIndex.search(q)
            return [res.dict for res in results]
        except SystemExit:
            raise ValidationException(detail=f"Failed to search for {q}")
