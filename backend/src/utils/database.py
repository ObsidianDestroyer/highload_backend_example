import asyncio

from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

from backend.settings import DEPLOY_ENV, SQLITE_PATH
from backend.src.utils.logger import logger


async def init_db() -> None:
    models = ['backend.src.models.actions_model', 'backend.src.models.user_model']
    logger.debug('models directories', directories=models)
    if DEPLOY_ENV == 'PROD':
        try:
            logger.warning(
                'processing database initialization', environment=DEPLOY_ENV
            )
            from backend.settings import (
                DB_HOST,
                DB_NAME,
                DB_PASSWORD,
                DB_PORT,
                DB_USER,
            )

            logger.debug(
                'processing ORM initialization', host=DB_HOST, port=DB_PORT
            )
            await Tortoise.init(
                config={
                    'connections': {
                        'default': {
                            'engine': 'tortoise.backends.mysql',
                            'credentials': {
                                'database': DB_NAME,
                                'host': DB_HOST,
                                'port': DB_PORT,
                                'user': DB_USER,
                                'password': DB_PASSWORD,
                            },
                        }
                    },
                    'apps': {
                        'models': {
                            'models': models,
                            'default_connection': 'default',
                        }
                    },
                }
            )
            logger.info('initialization completed', environment=DEPLOY_ENV)
        except DBConnectionError as db_err:
            logger.error('failed init connection database', host=DB_HOST)
            logger.warning('reconnect attempt', attempt_after=10)
            await asyncio.sleep(10)
            return await init_db()
    else:
        logger.warning(
            'processing database initialization', environment=DEPLOY_ENV
        )
        await Tortoise.init(
            db_url=f'sqlite://{SQLITE_PATH}', modules={'models': models}
        )
        logger.info('initialization completed', environment=DEPLOY_ENV)

    await Tortoise.generate_schemas()
    logger.debug('models schemas was generated . . .')


async def stop_db() -> None:
    logger.warning('closing database connections')
    await Tortoise.close_connections()
    logger.info('database connections closed')
