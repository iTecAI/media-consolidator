from typing import Dict
import requests
import time
import hashlib
from models import BaseModel

class PodcastEpisodeModel(BaseModel):
    def __init__(
        self,
        uuid: str | None = None,
        id: int = None,
        feedId: int = None,
        title: str = None,
        link: str = None,
        datePublished: int = None,
        enclosureUrl: str = None,
        enclosureType: str = None,
        duration: int = None,
        explicit: bool = None,
        episode: int = None,
        episodeType: str = None,
        season: int = None,
        image: str = None,
        **kwargs,
    ):
        super().__init__(uuid, **kwargs)
        self.id = id
        self.feedId = feedId
        self.title = title
        self.link = link
        self.datePublished = datePublished
        self.enclosureUrl = enclosureUrl
        self.enclosureType = enclosureType
        self.duration = duration
        self.explicit = explicit
        self.episode = episode
        self.episodeType = episodeType
        self.season = season
        self.image = image

class PodcastModel(BaseModel):
    def __init__(
        self,
        uuid: str | None = None,
        id: int = None,
        title: str = None,
        url: str = None,
        originalUrl: str = None,
        link: str = None,
        description: str = None,
        author: str = None,
        ownerName: str = None,
        image: str = None,
        artwork: str = None,
        contentType: str = None,
        language: str = None,
        categories: Dict[int, str] = None,
        lastScrape: float = 0,
        **kwargs,
    ):
        super().__init__(uuid, **kwargs)
        self.id = id
        self.title = title
        self.url = url
        self.originalUrl = originalUrl
        self.link = link
        self.description = description
        self.author = author
        self.ownerName = ownerName
        self.image = image
        self.artwork = artwork
        self.contentType = contentType
        self.language = language
        self.categories = categories
        self.lastScrape = lastScrape

    def get_episodes(self, index, use_last_scrape=False) -> list[PodcastEpisodeModel]:
        res = index.get_episodes(self.id, since=(self.lastScrape if use_last_scrape else 0))
        if use_last_scrape:
            self.lastScrape = time.time()
        
        return res


class Index:
    BASE_URL: str = "https://api.podcastindex.org/api/1.0/{path}"

    def __init__(
        self, token: str, secret: str, user_agent: str, debug_mode: bool = False
    ) -> None:
        self.token = token
        self.secret = secret
        self.user_agent = user_agent
        self.debug_mode = debug_mode

    def _make_headers(self):
        return {
            "User-Agent": self.user_agent,
            "X-Auth-Key": self.token,
            "X-Auth-Date": str(round(time.time())),
            "Authorization": hashlib.sha1(
                (self.token + self.secret + str(round(time.time()))).encode("utf-8")
            ).hexdigest(),
        }

    def search(self, term: str, clean: bool = False) -> list[PodcastModel]:
        response = requests.get(
            self.BASE_URL.format(path="search/byterm"),
            params={"q": term, "clean": clean, "pretty": self.debug_mode},
            headers=self._make_headers(),
        )

        if response.status_code == 200:
            raw = response.json()["feeds"]
            return [PodcastModel.from_dict(feed) for feed in raw]

        else:
            raise ConnectionError(
                f"Failed to search for {term} with status code {response.status_code} and error:\n\n{response.text}"
            )

    def get_episodes(self, feed_id: int, since: int = 0) -> list[PodcastEpisodeModel]:
        response = requests.get(
            self.BASE_URL.format(path="episodes/byfeedid"),
            params={
                "pretty": self.debug_mode,
                "id": feed_id,
                "since": since,
                "fulltext": True,
                "max": 1000,
            },
            headers=self._make_headers(),
        )

        if response.status_code == 200:
            raw = response.json()["items"]
            return [PodcastEpisodeModel.from_dict(ep) for ep in raw]

        else:
            raise ConnectionError(
                f"Failed to fetch episodes from feed {feed_id} with status code {response.status_code} and error:\n\n{response.text}"
            )
