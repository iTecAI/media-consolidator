from time import time
from typing import Any, Dict
from starlite import Starlite, get
from util import ApplicationState
import json
import os
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from keycloak import Keycloak
from controllers import *
from fastapi_restful.tasks import repeat_every

DB: Database = None
CONFIG = None


def load_app(state: ApplicationState):
    global DB, CONFIG
    if "CONSOLIDATOR_CONFIG" in os.environ.keys():
        cfg_path = os.environ["CONSOLIDATOR_CONFIG"]
    else:
        cfg_path = "config.json"
    with open(cfg_path, "r") as f:
        state.config = json.load(f)
        CONFIG = state.config.copy()

    _client = MongoClient(
        host=state.config["database"]["host"],
        port=state.config["database"]["port"],
        username=state.config["database"]["username"],
        password=state.config["database"]["password"],
    )

    state.database = _client[state.config["database"]["database"]]
    DB = _client[state.config["database"]["database"]]

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


@repeat_every(seconds=30)
def check_connections():
    global DB
    if DB:
        DB.connections.delete_many({"expiration": {"$lt": time()}})


app = Starlite(
    route_handlers=[get_root, LoginController, AccountController],
    on_startup=[load_app, check_connections],
)
