import typing as t

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from backend.src.guards import actions_guard, apply_guards
from backend.src.tasks.database_tasks import commit_action
from backend.src.utils.helpers.data_helper import (
    get_and_render_actions,
)
from backend.src.utils.logger import logger


async def apply_action(request: Request) -> t.Union[JSONResponse, Response]:
    logger.debug(
        'incoming request', request=request.url, method=request.method
    )

    is_done = await commit_action(request)
    if is_done:
        return Response(status_code=200)
    else:
        return JSONResponse({'error': 'user not found'}, status_code=400)


async def get_actions(request: Request) -> JSONResponse:
    logger.debug(
        'incoming request', request=request.url, method=request.method
    )
    actions = await get_and_render_actions()
    return JSONResponse(actions, status_code=200)


guarded_action_apply: t.Callable = apply_guards(apply_action, actions_guard)
