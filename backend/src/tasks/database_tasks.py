import asyncio
import typing as t

from starlette.requests import Request

from backend.settings import WRITING_PERIOD
from backend.src.models import Actions, User
from backend.src.utils.logger import logger

pending_actions: t.List[dict] = []
'''
    pending_action: dict = {
        'UID': <src.models.user_model.User>,    :type: object(Model)
        'actionType': 'VIEW',                   :type: str
        'page': '/'                             :type: str
    }
'''
running_tasks: t.List[t.Coroutine] = []


async def commit_action(request: Request) -> bool:
    existing_user = await User.filter(uid=request.query['UID']).first()
    if not existing_user:
        return False
    request.query['UID'] = existing_user
    pending_actions.append(dict(request.query))
    return True


async def run_database_tasks() -> None:
    tasks: t.List[asyncio.Future] = [periodic_writer]
    logger.info('starting background tasks', task=tasks)
    for task in tasks:
        logger.warning('invoking task', task=task)
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        asyncio.run_coroutine_threadsafe(periodic_writer(), loop=loop)


async def periodic_writer() -> None:
    logger.info(
        'started periodic DB writer', pending_actions=len(pending_actions)
    )
    while True:
        if len(pending_actions) == 0:
            logger.warning(
                'no pending actions to record',
                running_tasks=len(running_tasks),
            )
        for action in pending_actions:
            await (
                await Actions.filter(
                    path=action['page'], user=action['UID']
                ).first()
            ).update_action_count(name=action['actionType'])
            logger.debug(
                'processed action update', pending_actions=pending_actions
            )
            pending_actions.remove(action)
        await asyncio.sleep(WRITING_PERIOD)


async def stop_tasks() -> None:
    logger.debug('stopping writer task')
    for task in running_tasks:
        if isinstance(task, t.Coroutine):
            task.close()
        else:
            task: asyncio.Future
            task.cancel()
