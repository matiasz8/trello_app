import logging

from pydantic import ValidationError

from models.trello import TaskCard
from services.trello_service import TrelloService

logger = logging.getLogger(__name__)


class TaskService:
    """Service who handle Task data."""

    default_msg = "Validation rejected."

    @classmethod
    def publish_task(cls, payload: dict) -> str:
        """Task method handle."""
        try:
            result = TaskCard(**dict(payload))
        except (ValidationError, Exception) as e:
            result = e.errors()
        service_trello = TrelloService()
        print(service_trello.board_key)
        return result

