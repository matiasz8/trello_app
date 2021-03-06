from fastapi import APIRouter

from app.controllers import trello_controller as router_trello
from app.core.config import API_PREFIX

api_router = APIRouter(prefix=API_PREFIX)
api_router.include_router(router_trello.router, tags=["trello"], prefix="/trello")
