import logging
import requests
from config import DOMAIN, ORGANIZATION_ID
from src.exceptions import RequestError


class ResponseRole:
    def __init__(self, response) -> None:
        self.__response = response

    @property
    def key(self):
        return self.__response.get("key")

    @property
    def name(self):
        return self.__response.get("name")


class ResponseOrganization:
    def __init__(self, response) -> None:
        self.__response = response

    @property
    def roles(self):
        _roles = self.__response.get("roles")
        return [ResponseRole(r) for r in _roles]


class Organization:
    def __init__(self, token):
        self.__token = token

    def get_user_roles(self, uder_id):
        url = f"https://{DOMAIN}.kinde.com/api/v1/organizations/{ORGANIZATION_ID}/users/{uder_id}/roles"
        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__token}",
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if 200 <= response.status_code <= 399:
            return ResponseOrganization(response.json()).roles
        message = "Couldn't return the user profile."
        logging.error(message)
        raise RequestError("Couldn't return the user profile.")
