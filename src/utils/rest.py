import requests
import json


BASE_URL = "http://minikube:30501/"
HEADERS = {"Content-Type": "application/json"}


# https://github.com/pyscript/pyscript/pull/151/commits/3e3f21c08fa0a5e081804e8fbb11e708ee2813ce
async def request(
    url,
    method="GET",
    body=None,
    headers=None,
):
    """
    Async request function. Pass in Method and make sure to await!
    Parameters:
        method: str = {"GET", "POST", "PUT", "DELETE"} from javascript global fetch())
        body: str = body as json string. Example, body=json.dumps(my_dict)
        header: dict[str,str] = header as dict, will be converted to string...
            Example, header:json.dumps({"Content-Type":"application/json"})
    Return:
        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.
    """
    from pyodide.http import pyfetch, FetchResponse

    kwargs = {"method": method, "mode": "cors"}
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = json.dumps(body)
    if headers:
        kwargs["headers"] = headers

    response = await pyfetch(url, **kwargs)
    return response


async def get_all(resources):
    return await request(
        f"{BASE_URL}{resources}",
        "GET",
    )


def get_all_(resources):
    url = f"{BASE_URL}{resources}"
    response = requests.request("GET", url, headers={}, data={})
    return response.json()


def get_by_query(resources, query):
    url = f"{BASE_URL}{resources}?{query}"
    response = requests.request("GET", url, headers={}, data={})
    if response.status_code == 200:
        return response.json()
    return ValueError(f"Request has failed: {response.json()}")


async def get(resources, id):
    return await request(
        f"{BASE_URL}{resources}?id=eq.{str(id)}",
        "GET",
    )


def get_(resources, id):
    url = f"{BASE_URL}{resources}?id=eq.{str(id)}"
    response = requests.request("GET", url, headers={}, data={})
    return response.json()[0]


async def post(resources, data):
    return await request(
        f"{BASE_URL}{resources}",
        "POST",
        data,
        {"Content-Type": "application/json"},
    )


async def post_working(resources, data):
    from pyodide.http import pyfetch, FetchResponse

    url = f"{BASE_URL}{resources}"
    body = json.dumps(data)
    method = "POST"
    headers = HEADERS
    kwargs = {"method": method, "mode": "cors"}
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers

    response = await pyfetch(url, **kwargs)
    return response


def post_not_working_on_ui(resources, data):
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    url = f"{BASE_URL}{resources}"
    headers = HEADERS
    # return requests.request("POST", url, headers=headers, data=json.dumps(data))
    return session.post(url, headers=headers, data=json.dumps(data))


def patch(resources, id, data):
    url = f"{BASE_URL}{resources}?id=eq.{id}"
    headers = HEADERS
    return requests.request("PATCH", url, headers=headers, data=json.dumps(data))
