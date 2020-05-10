import typing as t

from backend.src.models import Actions


async def get_and_render_actions() -> t.List[t.Dict]:
    """
        Only for 'get_actions' route method at:
        routes.actions_routes.get_actions
    """
    actions = {}
    for action in await Actions.all():
        user_uid = (await action.user).UID
        if user_uid not in actions:
            actions[user_uid] = []
        actions[user_uid].append(action.render())
    return actions
