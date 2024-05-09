import logging
import requests
from config import DOMAIN
from src.exceptions import RequestError


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
        if 200 <= response.status_code <= 399:
            return ResponseUserProfile(response.json())
        message = "Couldn't return the user profile."
        logging.error(message)
        raise RequestError("Couldn't return the user profile.")
