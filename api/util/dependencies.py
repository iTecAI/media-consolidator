from typing import Any
from starlite import Request


def uuid_dep(request: Request[Any]) -> str | None:
    print(request.headers)
    if not "authorization" in request.headers.keys():
        return None
    if not "Bearer " in request.headers["authorization"]:
        return None

    return request.headers["authorization"].split("Bearer ")[1]
