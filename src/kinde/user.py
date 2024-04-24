import requests
from config import DOMAIN


class User:
    def __init__(self, token):
        self.__token = token

    def get_by_id(self, user_id):
        url = f"https://{DOMAIN}.kinde.com/api/v1/user?id={user_id}"
        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__token}",
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_all(self):
        url = f"https://{DOMAIN}.kinde.com/api/v1/users"
        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__token}",
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()
