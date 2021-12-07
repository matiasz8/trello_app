import logging

from pydantic import ValidationError

from app.models.trello import TaskCard
from app.services.trello_service import service_trello

logger = logging.getLogger(__name__)


class TaskService():
    """Service who handle Task data."""

    @classmethod
    def publish_task(cls, payload: dict) -> str:
        """A task:
            This represents some manual work that needs to be done.
            It will count with just a title and a category (Maintenance, Research, or Test)
            Each corresponding to a label in trello.
        """
        try:
            result = TaskCard(**dict(payload))
        except (ValidationError, Exception) as e:
            result = e.errors()
        card = service_trello.create_card(
            card_name=result.title,
            category=result.category
        )
        return card
