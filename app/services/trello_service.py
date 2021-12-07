import requests
import json

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
        if resp.status_code == 200:
            try:
                resp = json.loads(resp.text)
                boards = BoardList(boards=resp)
            except ValidationError as val_err:
                return val_err.errors()
            return boards
        else:
            raise ConnectionError(resp.text)

    def get_board_by_default_name(self):
        try:
            board_list = self.get_boards()
        except ConnectionError as conn_err:
            raise conn_err

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
        resp = self.__client.boards.new(name=board_name)
        return resp.id

    def create_card(self, card_name, idList=1):
        resp = self.__client.cards.new(name=card_name,idList=idList)
        return resp

service_trello = TrelloService()
