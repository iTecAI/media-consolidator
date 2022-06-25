from starlite import Starlite
from util import ApplicationState
import json
import os
from pymongo.mongo_client import MongoClient
from keycloak import Keycloak


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
            state.config["authSource"]["keycloak"]["sso"],
            state.config["authSource"]["keycloak"]["clientId"],
            state.config["authSource"]["keycloak"]["clientSecret"],
        )


if __name__ == "__main__":
    app = Starlite(route_handlers=[], on_startup=[load_app])
