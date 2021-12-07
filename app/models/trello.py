from enum import Enum

from typing import Optional, List
from pydantic import BaseModel, validator, Field


class Types(str, Enum):
    task = "task"
    issue = "issue"
    bug = "bug" 


class TrelloType(BaseModel):
    type: Types


class TrelloCard(TrelloType):  # type: ignore
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]


class IssueCard(TrelloType):  # type: ignore
    title: str = Field(..., max_length=40, min_length=4)
    description: str = Field(..., max_length=3000, min_length=10)


class BugCard(TrelloType):  # type: ignore
    description: str = Field(..., max_length=3000, min_length=10)


class TaskCard(TrelloType):  # type: ignore
    title: str = Field(..., max_length=40, min_length=4)
    category: str = Field(..., max_length=20, min_length=4)

    @validator("category")  # type: ignore
    @classmethod
    def check_category(cls, val: str) -> str:
        val = val.capitalize()
        categories = ["Maintenance", "Research", "Test"]
        assert val in categories, f"Category [{val}] not found. Try with: {categories}"
        return val


class Item(BaseModel):
    id: str
    name: str


class TrelloLists(BaseModel):  # type: ignore
    items: List[Item]

