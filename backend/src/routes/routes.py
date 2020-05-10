import typing as t

from starlette.routing import Route

from backend.src.routes.actions_route import (
    get_actions,
    guarded_action_apply,
)


def get_routes() -> t.List[Route]:
    routes = [
        Route('/api/action', endpoint=guarded_action_apply, methods=['POST']),
        Route('/api/action', endpoint=get_actions, methods=['GET']),
    ]
    return routes
