
import pytest
from pydantic import ValidationError

from app.models.trello import TrelloCard, TrelloLists


class TestModels():
    """Test trello model."""

    def test_trello_type(self):
        data = {
            "type": "task",
            "title": "title test",
            "description": "description test",
            "category": "category test"
        }
        result = TrelloCard(**data)
        assert result
        data.update({"type": "issue"})
        result = TrelloCard(**data)
        assert result
        data.update({"type": "bug"})
        result = TrelloCard(**data)
        assert result

        error = "value is not a valid enumeration member; permitted: 'task', 'issue', 'bug'"
        try:
            data.update({"type": "invalid type"})
            result = TrelloCard(**data)
            assert result
        except ValidationError as val_err:
            assert val_err.errors()[0]["msg"] == error

    def test_board_labels_lists(self):
        data = [
            {
                "name": "002",
                "id": "5db91d55cc2d210ef01a7ba6"
            }
        ]
        error = [{'loc': ('items', 0), 'msg': 'value is not a valid dict', 'type': 'type_error.dict'}]
        board_list = TrelloLists(items=data)
        assert board_list
        try:
            data = ["121212"]
            board_list = TrelloLists(items=data)
        except ValidationError as val_err:
            assert error == val_err.errors()
