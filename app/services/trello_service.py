import requests
import json

from pydantic import ValidationError
from trello import TrelloApi


from core.config import (
    TRELLO_APP_KEY,
    TRELLO_APP_TOKEN,
    TRELLO_DEFAULT_BOARD,
    TRELLO_DEFAULT_LIST,
    TRELLO_BASE_URL
)
from models.trello import Board_And_List


class TrelloService:
    def __init__(self):
        self.__client = TrelloApi(TRELLO_APP_KEY, TRELLO_APP_TOKEN)
        self.board_key = self.get_or_create_board()
        self.list_key = self.get_or_create_list()

    def raise_or_json(self, resp):
        resp.raise_for_status()
        return resp.json()

    def get_boards(self):
        """Get all boards"""
        resp = requests.get(
            f"{TRELLO_BASE_URL}/members/me/boards?",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN, 
                "fields": ["name"]})
        return self.raise_or_json(resp)

    def get_or_create_board(self):
        try:
            resp = self.get_boards()
        except ConnectionError as conn_err:
            raise conn_err
        try:
            board_list = Board_And_List(items=resp)
        except ValidationError as val_err:
            raise val_err.errors()

        # case I: empty list
        if not board_list:
            return self.create_board()

        # case II: key could be in the list
        for value in board_list.items:
            if value.name == TRELLO_DEFAULT_BOARD:
                return value.id

        # case III: key not be in the list
        return self.create_board()

    def create_board(self, board_name=TRELLO_DEFAULT_BOARD):
        resp = self.__client.boards.new(name=board_name)
        return resp["id"]

    def get_lists(self):
        """Get all lists"""
        resp = requests.get(
            f"{TRELLO_BASE_URL}/boards/{self.board_key}/lists?",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN, 
                "fields": ["name"]
            }
        )
        return self.raise_or_json(resp)

    def get_or_create_list(self):
        try:
            resp = self.get_lists()
        except ConnectionError as conn_err:
            raise conn_err
        try:
            lists = Board_And_List(items=resp)
        except ValidationError as val_err:
            raise val_err.errors()

        # case I: empty list
        if not lists:
            print("no hay listas")
            return self.create_list()

        # case II: key could be in the list
        for value in lists.items:
            if value.name == TRELLO_DEFAULT_LIST:
                return value.id

        # case III: key not be in the list

        return self.create_list()

    def create_list(self, list_name=TRELLO_DEFAULT_LIST):
        resp = self.__client.lists.new(name=list_name, idBoard=self.board_key)
        return resp["id"]

    def create_card(self, card_name, category=None, description=None):
        resp = self.__client.cards.new(
            name=card_name,
            idList=self.list_key,
            idLabels=category,
            desc=description,
        )
        if resp.status_code == 400:
            print(resp.text)
        return resp

service_trello = TrelloService()
