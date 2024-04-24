import requests
from config import DOMAIN


class ResponseUserProfile:
    def __init__(self, response):
        self.__response = response

    @property
    def id(self):
        return self.__response.get("id")


class UserProfile:
    def __init__(self, token):
        self.__token = token

    def get(self):
        url = f"https://{DOMAIN}.kinde.com/oauth2/user_profile"
        payload = {}
        headers = {"Authorization": f"Bearer {self.__token}"}
        response = requests.request("GET", url, headers=headers, data=payload)
        return ResponseUserProfile(response.json())
