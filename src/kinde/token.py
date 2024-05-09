import requests
from config import DOMAIN


class Token:

    def get(self):
        class ResponseToken:
            def __init__(self, token):
                self.__token = token

            @property
            def access_token(self):
                return self.__token.get("access_token")

        url = f"https://{DOMAIN}.kinde.com/oauth2/token"
        payload = f"audience=https%3A%2F%2F{DOMAIN}.kinde.com%2Fapi&grant_type=client_credentials&client_id=3d09ff7a5bdc45cb92e64f92a0081b34&client_secret=GUhsfKyikN1jJVfgmPRhluzXu2ajFaJrdyHpi5Y59XFxnlxiYzup2"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return ResponseToken(response.json())
