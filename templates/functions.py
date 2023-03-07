from datetime import datetime
from pyscript import Element, create
from pyodide.http import pyfetch, FetchResponse


BASE_URL = "http://minikube:30500"
CONTENT_TYPE = "application/json"


# https://github.com/pyscript/pyscript/pull/151/commits/3e3f21c08fa0a5e081804e8fbb11e708ee2813ce
async def request(
    url,
    method = "GET",
    body = None,
    headers = None,
) -> FetchResponse:
    """
    Async request function. Pass in Method and make sure to await!
    Parameters:
        method: str = {"GET", "POST", "PUT", "DELETE"} from javascript global fetch())
        body: str = body as json string. Example, body=json.dumps(my_dict)
        header: dict[str,str] = header as dict, will be converted to string...
            Example, header:json.dumps({"Content-Type":CONTENT_TYPE})
    Return:
        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.
    """
    kwargs = {"method": method, "mode": "cors"}
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers

    response = await pyfetch(url, **kwargs)
    return response


async def poc_postgrest():
    url = "http://minikube:30501/alunos"
    response = await request(url, "GET")
    output = f"GET request=> status:{response.status}, json:{await response.json()}"
    __update_terminal(output, "INFO")


def __update_terminal(text, message_type):
    terminal = Element("local-terminal")
    item = create("pre", classes="py-p")
    item.element.innerText = f"{datetime.now()} {message_type} {text}"
    terminal.element.appendChild(item.element)
    terminal.element.insertBefore(item.element, terminal.element.childNodes[0])
