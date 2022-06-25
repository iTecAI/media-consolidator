from typing import Any, Dict
from starlite import Starlite, get
from util import ApplicationState
import json
import os
from pymongo.mongo_client import MongoClient
from keycloak import Keycloak
from controllers import *


def load_app(state: ApplicationState):
    if "CONSOLIDATOR_CONFIG" in os.environ.keys():
        cfg_path = os.environ["CONSOLIDATOR_CONFIG"]
    else:
        cfg_path = "config.json"
    with open(cfg_path, "r") as f:
        state.config = json.load(f)

    _client = MongoClient(
        host=state.config["database"]["host"],
        port=state.config["database"]["port"],
        username=state.config["database"]["username"],
        password=state.config["database"]["password"],
    )

    state.database = _client[state.config["database"]["database"]]

    if "keycloak" in state.config["authSource"]["modes"]:
        state.keycloak = Keycloak(
            state.config["authSource"]["keycloak"]["url"],
            state.config["authSource"]["keycloak"]["realm"],
            state.config["authSource"]["keycloak"]["clientId"],
            state.config["authSource"]["keycloak"]["clientSecret"],
        )


@get("/")
async def get_root() -> Dict[str, Any]:
    return {"status": "running"}


app = Starlite(
    route_handlers=[get_root, LoginController, AccountController], on_startup=[load_app]
)
