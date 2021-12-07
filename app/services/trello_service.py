import requests

from pydantic import ValidationError
from trello import TrelloApi


from core.config import (
    TRELLO_APP_KEY,
    TRELLO_APP_TOKEN,
    TRELLO_DEFAULT_BOARD,
    TRELLO_BASE_URL
)
from models.trello import BoardList


class TrelloService:
    def __init__(self):
        self.__client = TrelloApi(TRELLO_APP_KEY, TRELLO_APP_TOKEN)
        self.board_key = self.get_board_by_default_name()

    def get_board(self, board_id):
        """Get a contact from bitrix"""
        return self.__client.boards.get(board_id)

    def get_boards(self):
        """Get all boards"""
        resp = requests.get(
            f"{TRELLO_BASE_URL}/members/me/boards?",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN, 
                "fields": ["name"]})
        try:
            boards = BoardList(boards=resp)
        except ValidationError as val_err:
            return val_err.errors()
        return boards

    def get_board_by_default_name(self):
        board_list = self.get_boards()

        # case I: empty list
        if not board_list:
            return self.create_board()

        # case II: key could be in the list
        for value in board_list.boards:
            if value.name == TRELLO_DEFAULT_BOARD:
                return value.id

        # case III: key not be in the list
        return self.create_board()

    def create_board(self, board_name=TRELLO_DEFAULT_BOARD):
        resp = requests.post(
            f"{TRELLO_BASE_URL}boards/",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN, 
                "name": board_name
            }
        )
        board_id = response.json()["shortUrl"].split("/")[-1].strip()
        return board_id
