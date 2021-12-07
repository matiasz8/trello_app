import logging
import requests
import json

from pydantic import ValidationError
from trello import TrelloApi

from app.core.config import (
    TRELLO_APP_KEY,
    TRELLO_APP_TOKEN,
    TRELLO_DEFAULT_BOARD,
    TRELLO_DEFAULT_LIST,
    TRELLO_BASE_URL,
    TRELLO_DEFAULT_LABELS
)
from app.models.trello import TrelloLists, MemberLists


logger = logging.getLogger(__name__)


class TrelloService:
    def __init__(self):
        self.__client = TrelloApi(TRELLO_APP_KEY, TRELLO_APP_TOKEN)
        self.board_key = self.get_or_create_board()
        self.list_key = self.get_or_create_list()
        self.label_maintenance = self.get_or_create_label("Maintenance")
        self.label_research = self.get_or_create_label("Research")
        self.label_test = self.get_or_create_label("Test")
        self.label_bug = self.get_or_create_label("Bug")

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
            board_list = TrelloLists(items=resp)
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
            lists = TrelloLists(items=resp)
        except ValidationError as val_err:
            raise val_err.errors()

        # case I: empty list
        if not lists:
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

    def get_labels(self):
        """Get all labels"""
        resp = requests.get(
            f"{TRELLO_BASE_URL}/boards/{self.board_key}/labels",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN,
                "fields": ["name"]})
        return self.raise_or_json(resp)

    def get_or_create_label(self, category: str):
        try:
            resp = self.get_labels()
        except ConnectionError as conn_err:
            raise conn_err
        try:
            label_list = TrelloLists(items=resp)
        except ValidationError as val_err:
            raise val_err.errors()

        # case I: empty list
        if not label_list:
            return self.create_label(category)

        # case II: key could be in the list
        for value in label_list.items:
            if value.name == category:
                return value.id

        # case III: key not be in the list
        return self.create_label(category)

    def create_label(self, label):
        label_color = TRELLO_DEFAULT_LABELS[label]["color"]
        resp = self.__client.labels.new(
            name=label,
            color=label_color,
            idBoard=self.board_key
        )
        return resp["id"]

    def get_labels_ids(self, category):
        data = {
            "Bug": self.label_bug,
            "Test": self.label_test,
            "Research": self.label_research,
            "Maintenance": self.label_maintenance
        }
        return data[category]

    def get_members(self):
        """Get all members"""
        resp = requests.get(
            f"{TRELLO_BASE_URL}/boards/{self.board_key}/members",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN,
                "fields": ["id"]})
        return self.raise_or_json(resp)

    def get_member_for_list(self):
        try:
            resp = self.get_members()
        except ConnectionError as conn_err:
            raise conn_err
        try:
            members = MemberLists(items=resp)
        except ValidationError as val_err:
            logger.info(val_err.errors())
            return None

        # case I: empty list
        if not members:
            return None

        for value in members.items:
            return value.id

    def create_card(self, card_name, category=None, description=None, assing_member=None):
        if category:
            category = self.get_labels_ids(category)

        resp = requests.post(
            f"{TRELLO_BASE_URL}/cards",
            params={
                "key": TRELLO_APP_KEY,
                "token": TRELLO_APP_TOKEN,
                "idList": self.list_key,
                "idMembers": assing_member
            },
            json={
                "name": card_name,
                "desc": description,
                "idLabels": category
            }
        )
        return self.raise_or_json(resp)


service_trello = TrelloService()
