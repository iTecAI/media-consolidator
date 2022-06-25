from typing import Any
from starlite import Controller, NotFoundException, Provide, get
from starlite.datastructures import State
from util import guard_loggedIn, uuid_dep
from models import *


class AccountController(Controller):
    path = "/account"
    guards = [guard_loggedIn]
    tags = ["account"]
    dependencies = {"uuid": Provide(uuid_dep)}

    @get(media_type="application/json")
    async def get_account_info(self, state: State, uuid: str | None) -> Any:
        if uuid:
            try:
                result = SessionInfo.from_uuid(state.database, uuid)
                return result.dict
            except TypeError:
                pass

        raise NotFoundException(detail=f"Could not locate connection with UUID {uuid}")
