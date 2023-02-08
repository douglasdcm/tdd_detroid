import requests
import json

BASE_URL = "http://minikube:30501/"
HEADERS = {"Content-Type": "application/json"}


def get_all(resources):
    url = f"{BASE_URL}{resources}"
    response = requests.request("GET", url, headers={}, data={})
    return response.json()


def get_by_query(resources, query):
    url = f"{BASE_URL}{resources}?{query}"
    response = requests.request("GET", url, headers={}, data={})
    if response.status_code == 200:
        return response.json()
    return ValueError(f"Request has failed: {response.json()}")


def get(resources, id):
    url = f"{BASE_URL}{resources}?id=eq.{str(id)}"
    response = requests.request("GET", url, headers={}, data={})
    return response.json()[0]


def post(resources, data):
    url = f"{BASE_URL}{resources}"
    headers = HEADERS
    return requests.request("POST", url, headers=headers, data=json.dumps(data))


def patch(resources, id, data):
    url = f"{BASE_URL}{resources}?id=eq.{id}"
    headers = HEADERS
    return requests.request("PATCH", url, headers=headers, data=json.dumps(data))
