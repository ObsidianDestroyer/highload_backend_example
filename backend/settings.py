from backend.src.utils.env import env_or_exit

DEBUG_MODE = env_or_exit('DEBUG_MODE', cast=bool)
DEPLOY_ENV = env_or_exit('DEPLOY_ENV', cast=str)
SQLITE_PATH = env_or_exit('SQLITE_PATH', cast=str)
WRITING_PERIOD = env_or_exit('WRITING_PERIOD', cast=int)
DB_HOST = env_or_exit('DB_HOST', cast=str)
DB_NAME = env_or_exit('DB_NAME', cast=str)
DB_PASSWORD = env_or_exit('DB_PASSWORD', cast=str)
DB_PORT = env_or_exit('DB_PORT', cast=str)
DB_USER = env_or_exit('DB_USER', cast=str)
