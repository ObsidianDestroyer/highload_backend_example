import typing as t

from backend.src.models import Actions, User
from backend.src.utils.logger import logger


async def create_users() -> None:
    users = [
        {'name': 'Walther'},
        {'name': 'Stefan'},
        {'name': 'Miguel'},
        {'name': 'Nikel'},
    ]
    logger.warning('pre-creating users records', amount=len(users))
    for user in users:
        user_name = user['name']
        existing_user = await User.filter(name=user_name).first()
        if not existing_user:
            await User.create(name=user_name)
        else:
            logger.warning(f'user {user_name!r} exists', id=existing_user.UID)
            # NOTE: 'continue' needs to block event loop for prevent
            #   requests before backend start
            continue


async def create_pages() -> None:
    pages = [
        {'path': '/'},
        {'path': '/messages'},
        {'path': '/statistics'},
        {'path': '/profile'},
        {'path': '/notifications'},
        {'path': '/news'},
    ]
    logger.warning('pre-creating pages records', amount=len(pages))
    for page in pages:
        page_path = page['path']
        users: t.List[User] = await User.all()
        existing_page_actions = await Actions.filter(path=page_path).first()
        if not existing_page_actions:
            for user in users:
                await Actions.create(path=page_path, user=user)
        else:
            logger.warning(
                f'page {page_path!r} exists', id=existing_page_actions.id
            )
            # NOTE: 'continue' needs to block event loop for prevent
            #   requests before backend start
            continue
