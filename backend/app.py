from starlette.applications import Starlette

from backend.settings import DEBUG_MODE
from backend.src.routes import get_routes
from backend.src.tasks.database_tasks import (
    run_database_tasks,
    stop_tasks,
)
from backend.src.tasks.startup_tasks import create_pages, create_users
from backend.src.utils.database import init_db, stop_db
from backend.src.utils.logger import logger

routes = [*get_routes()]


def create_app() -> Starlette:
    logger.debug('creating app instance', debug_mode=DEBUG_MODE)
    return Starlette(
        debug=DEBUG_MODE,
        routes=routes,
        on_startup=[init_db, create_users, create_pages, run_database_tasks],
        on_shutdown=[stop_db, stop_tasks]
    )


app = create_app()
