from time import time
from typing import Any
from starlite import Request, BaseRouteHandler
from starlite.exceptions import NotAuthorizedException, ValidationException
from .application_state import ApplicationState


def guard_loggedIn(request: Request[Any], handler: BaseRouteHandler) -> None:
    if not "authorization" in request.headers.keys():
        raise NotAuthorizedException(detail="No Authorization header passed.")

    if len(request.headers["authorization"].split("Bearer ")) != 2:
        raise ValidationException(detail="Bad Authorization format.")

    state: ApplicationState = request.app.state
    session = state.database.connections.find_one(
        {"uuid": request.headers["authorization"].split("Bearer ")[1]}
    )
    if not session:
        raise NotAuthorizedException(detail="Not logged in.")

    if time() > session["expiration"]:
        state.database.connections.delete_one(
            {"uuid": request.headers["authorization"].split("Bearer ")[1]}
        )
        raise NotAuthorizedException(detail="Not logged in.")

    state.database.connections.update_one(
        {"uuid": request.headers["authorization"].split("Bearer ")[1]},
        {"$set": {"expiration": time() + state.config["sessionExpiration"]}},
    )
