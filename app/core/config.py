import os
from typing import Dict

from starlette.config import Config

ROOT_DIR = os.getcwd()
_config = Config(os.path.join(ROOT_DIR, '.env'))
APP_VERSION = "0.0.1"
APP_NAME = "Trello Tasks"
API_PREFIX = "/v1"

# Env vars
IS_DEBUG: bool = _config("IS_DEBUG", cast=bool, default=True)

# ENV
ENV: str = _config("ENV", cast=str, default="")

TRELLO_APP_KEY: str = _config("TRELLO_APP_KEY", cast=str, default="")
TRELLO_APP_TOKEN: str = _config("TRELLO_APP_TOKEN", cast=str, default="")
TRELLO_DEFAULT_BOARD: str = _config("TRELLO_DEFAULT_BOARD", cast=str, default="TrelloTasks")
TRELLO_BASE_URL: str = _config("TRELLO_BASE_URL", cast=str, default="https://api.trello.com/1/")
