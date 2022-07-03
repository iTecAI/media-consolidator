from typing import Any, Dict, List
from starlite import Controller, Provide, get, ValidationException, State
from util import PodcastModel, uuid_dep, guard_loggedIn
from models import SearchResultModel
import difflib

class PodcastController(Controller):
    path: str = "/sources/podcasts"
    guards = [guard_loggedIn]
    tags = ["podcasts"]
    dependencies = {"uuid": Provide(uuid_dep)}

    @get(path="/search")
    async def search_podcasts(self, q: str, state: State) -> List[SearchResultModel]:
        try:
            results: List[PodcastModel] = state.podcastIndex.search(q)
            final = [{
                "title": res.title,
                "subtitle": res.author,
                "description": res.description,
                "image": res.image,
                "type": "podcasts",
                "reference": res.id,
                "canDownload": True,
                "canExpand": True,
                "canUpdate": True,
                "similarity": difflib.SequenceMatcher(a=res.title, b=q).ratio(),
                "lastDownload": res.lastScrape if res.lastScrape > 0 else None
            } for res in results]
            return final
        except SystemExit:
            raise ValidationException(detail=f"Failed to search for {q}")
