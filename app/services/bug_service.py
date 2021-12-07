import logging

from pydantic import ValidationError
from models.trello import BugCard


logger = logging.getLogger(__name__)


class BugService:
    """Service who handle Bug data."""

    default_msg = "Validation rejected."

    @classmethod
    def publish_bug(cls, payload: dict) -> str:
        """Bug method handle."""
        try:
            payload = BugCard(**dict(payload))
        except ValidationError as val_error:
            return val_error.errors()

        
