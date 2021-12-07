from fastapi import APIRouter, status, Depends

from models.trello import TrelloCard
from services.task_service import TaskService as service_task
from services.bug_service import BugService as service_bug
from services.issue_service import IssueService as service_issue


router = APIRouter()


@router.get("",
            name="Trello API",
            status_code=status.HTTP_200_OK,
            description="Api who provide an easily way to handle Trello Tasks"
            )
async def post_card(card: TrelloCard = Depends()):
    """Handle trello cards."""
    if card.type == "task":
        return service_task.publish_task(card)
    elif card.type == "bug":
        return service_bug.publish_bug(card)
    return service_issue().publish_issue(card)
