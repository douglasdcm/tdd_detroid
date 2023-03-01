from datetime import datetime
from pyscript import Element, create
from pyodide.http import pyfetch, FetchResponse
import json

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


async def subscribe_discipline():
    try:
        student_id = Element("subscribe-student-id").value
        discipline_id = Element("subscribe-discipline-id").value
        text = await request(
            f"{BASE_URL}/subscription-discipline",
            "POST",
            json.dumps({
                "student_id": student_id,
                "discipline_id": discipline_id
            }),
            {"Content-Type": CONTENT_TYPE},
        )
        __update_terminal(await text.json(), "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_discipline():
    try:
        name = Element("discipline-name").value
        course_id = Element("course-discipline-id").value
        text = await request(
            f"{BASE_URL}/discipline",
            "POST",
            json.dumps({
                "name": name,
                "course_id": course_id
            }),
            {"Content-Type": CONTENT_TYPE},
        )
        __update_terminal(await text.json(), "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def subscribe_course():
    try:
        student_id = Element("student-id").value
        course_id = Element("course-id").value
        text = await request(
            f"{BASE_URL}/subscription-course",
            "POST",
            json.dumps({
                "student_id": student_id,
                "course_id": course_id
            }),
            {"Content-Type": CONTENT_TYPE},
        )
        __update_terminal(await text.json(), "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_course():
    try:
        name = Element("course-name").value
        text = await request(
            f"{BASE_URL}/course",
            "POST",
            json.dumps({"name": name}),
            {"Content-Type": CONTENT_TYPE},
        )
        __update_terminal(await text.json(), "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_student():
    try:
        name = Element("student-name").value
        text = await request(
            f"{BASE_URL}/student",
            "POST",
            json.dumps({"name": name}),
            {"Content-Type": CONTENT_TYPE},
        )
        __update_terminal(await text.json(), "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def __update_terminal(text, message_type):
    terminal = Element("local-terminal")
    item = create("pre", classes="py-p")
    item.element.innerText = f"{datetime.now()} {message_type} {text}"
    terminal.element.appendChild(item.element)
    terminal.element.insertBefore(item.element, terminal.element.childNodes[0])
