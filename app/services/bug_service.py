import logging
import random
from random_word import RandomWords

from pydantic import ValidationError
from models.trello import BugCard

from services.trello_service import service_trello

logger = logging.getLogger(__name__)


class BugService:
    """Service who handle Bug data."""

    @classmethod
    def publish_bug(cls, payload: dict) -> str:
        """Bug method handle."""
        try:
            result = BugCard(**dict(payload))
        except ValidationError as val_error:
            return val_error.errors()

        member = service_trello.get_member_for_list()
        print(">>>>", member)
        card = service_trello.create_card(
            card_name=cls.get_random_title(),
            description=result.description,
            category="Bug",
            assing_member=member
        )
        return card

    @staticmethod
    def get_random_title():
        number = random.randint(0,1000)
        r = RandomWords()
        word = r.get_random_word()
        return f"bug-{word}-{number}"
