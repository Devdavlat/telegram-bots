import requests
import json

from environs import Env

env = Env()
env.read_env()


class TrelloManager:
    trello_api_key = env('TRELLO_API_KEY')
    trello_token = env('TRELLO_TOKEN')
    # print(trello_token)
    # print(trello_api_key)

    def __init__(self, username):
        self.username = username

    @staticmethod
    def base_header():
        return {
            "Accept": "application/json"
        }

    @staticmethod
    def get_list_id_with_name(list_id, name):
        try:
            return [data.get('name') for data in list_id if name == data.get('name')][0]
        except Exception as e:
            print(e)

    def credentials(self):
        return {
            "key": self.trello_api_key,
            'token': self.trello_token
        }

    def get_member_id(self):
        url = f"https://api.trello.com/1/members/{self.username}"

        response = requests.request(
            'GET',
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_board(self):

        url = f"https://api.trello.com/1/members/{self.username}/boards"

        response = requests.request(
            'GET',
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_list_on_a_board(self, board_id):

        url = f'https://api.trello.com/1/boards/{board_id}/lists'

        response = requests.request(
            'GET',
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        # print(response.status_code)
        if response.status_code == 200:
            return json.loads(response.text)

    def get_board_id_with_name(self, name):
        try:
            return [board.get('name') for board in self.get_board() if board.get('name') == name][0]
        except Exception as e:
            print(e)

    def get_board_members(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/memberships"

        response = requests.request(
            "GET",
            url,
            headers=self.base_header(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def get_cards_on_a_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        response = requests.request(
            "GET",
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)


# trello = TrelloManager('dav')
# print(trello.trello_token)
# print(trello.trello_api_key)