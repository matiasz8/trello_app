import logging

from pydantic import ValidationError
from models.trello import IssueCard


logger = logging.getLogger(__name__)


class IssueService:
    """Service who handle Issue data."""

    default_msg = "Validation rejected."

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
        return result

