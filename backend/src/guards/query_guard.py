from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.src.utils.logger import logger


async def actions_guard(request: Request) -> Request:
    query = dict(request.query_params)
    available_keys = ['page', 'actionType', 'UID']
    for a_key, q_key in zip(available_keys, query):
        if a_key in q_key:
            key = query.get(a_key)
            if key:
                continue
            else:
                logger.error(
                    'bad query params, request aborted',
                    url_path=request.url.path,
                    host=request.headers.get('Host'),
                    bad_key=q_key,
                )
                return JSONResponse(
                    {'error': 'Bad QUERY params'}, status_code=400
                )
    request.query = query
    return request
