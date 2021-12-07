from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


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


class Board(BaseModel):
    id: str
    name: str


class BoardList(BaseModel):  # type: ignore
    boards: List[Board]

