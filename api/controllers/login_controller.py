from time import time
from typing import Any, Dict
from requests import Response
from starlite.controller import Controller
from pydantic import UUID4, BaseModel
from util import ApplicationState
from starlite import NotAuthorizedException, State, post
import uuid
import hashlib
from starlette.status import *


class LoginModel(BaseModel):
    username: str
    password: str


class LoginController(Controller):
    path = "/login"

    def _successful_login(
        self, username: str, state: ApplicationState, scope: list[str], info
    ):
        connection_id = str(uuid.uuid4())
        state.database.connections.delete_many({"username": username})
        state.database.connections.insert_one(
            {
                "username": username,
                "scope": scope,
                "uuid": connection_id,
                "userInfo": info,
                "expiration": time() + state.config["sessionExpiration"],
            }
        )
        return connection_id

    @post()
    async def login(self, data: LoginModel, state: State) -> Dict[str, Any] | Response:
        """
        Route to login to application via configured methods
        """

        # Check authentication based on local user list
        if "local" in state.config["authSource"]["modes"]:
            if data.username in state.config["authSource"]["local"]["users"].keys():
                if (
                    data.password
                    == state.config["authSource"]["local"]["users"][data.username][
                        "password"
                    ]
                ):
                    user_info = {
                        "username": data.username,
                        "email": None,
                        "displayName": data.username,
                        "icon": f"https://www.gravatar.com/avatar/{hashlib.md5(data.username.encode('utf-8')).hexdigest()}?d=identicon",
                    }
                    return {
                        "uuid": self._successful_login(
                            data.username,
                            state,
                            state.config["userPerms"][data.username],
                            user_info,
                        ),
                        "permissions": state.config["userPerms"][data.username],
                        "userInfo": user_info,
                    }
                else:
                    raise NotAuthorizedException(
                        detail="Incorrect username or password"
                    )

        # Check authentication based on keycloak
        if "keycloak" in state.config["authSource"]["modes"] and state.keycloak != None:
            try:
                token = state.keycloak.auth(data.username, data.password)
            except:
                raise NotAuthorizedException(detail="Incorrect username or password")

            found = False
            for k in state.config["authSource"]["keycloak"]["scopes"]:
                if token.is_scoped(k):
                    found = True
                    break

            if not found:
                raise NotAuthorizedException(detail="Incorrect scope for application")

            if data.username in state.config["userPerms"].keys():
                perms = state.config["userPerms"][data.username]
            else:
                perms = []
                for scope in token.scope:
                    if scope in state.config["userPerms"].keys():
                        perms.extend(state.config["userPerms"][scope])

            user_info = token.info()
            info = {
                "username": data.username,
                "email": user_info.email,
                "displayName": user_info.name,
                "icon": f"https://www.gravatar.com/avatar/{hashlib.md5(user_info.email.encode('utf-8')).hexdigest()}?d=identicon",
            }
            user_id = self._successful_login(data.username, state, perms, info)

            return {
                "uuid": user_id,
                "permissions": perms,
                "userInfo": info,
            }

        raise NotAuthorizedException(detail="Incorrect username or password")
