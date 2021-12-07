import logging

from pydantic import ValidationError

from app.models.trello import IssueCard
from app.services.trello_service import service_trello


logger = logging.getLogger(__name__)


class IssueService:
    """Service who handle Issue data."""

    @classmethod
    def publish_issue(cls, payload: dict) -> str:
        """Issue method handle.

           An issue:
           This represents a business feature that needs implementation,
           they will provide a short title and a description.
           All issues gets added to the “To Do” list as unassigned
        """
        try:
            result = IssueCard(**dict(payload))
        except (ValidationError, Exception) as e:
            result = e.errors()

        card = service_trello.create_card(
            card_name=result.title,
            description=result.description
        )
        return card
