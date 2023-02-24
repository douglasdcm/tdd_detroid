from src.controllers import students
from src.controllers import disciplines
from datetime import datetime
from pyscript import Element, create
from pyodide.http import pyfetch, FetchResponse
from typing import Optional
import json

BASE_URL = "http://minikube:30500"

# https://github.com/pyscript/pyscript/pull/151/commits/3e3f21c08fa0a5e081804e8fbb11e708ee2813ce
async def request(
    url: str,
    method: str = "GET",
    body: Optional[str] = None,
    headers: Optional[dict[str, str]] = None,
) -> FetchResponse:
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
    kwargs = {"method": method, "mode": "cors"}
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers

    response = await pyfetch(url, **kwargs)
    return response


def subscribe_discipline():
    try:
        student_id = Element("subscribe-student-id")
        materia_id = Element("subscribe-discipline-id")
        students.subscribe_in_discipline(student_id.value, materia_id.value)
        qtde = len(students.get_all())
        text = f"#Student id {qtde}, Name {students.get(qtde).nome}, Discipline id {disciplines.get(qtde).materia_id}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_discipline():
    try:
        discipline_nome = Element("discipline-nome")
        curso_discipline_id = Element("course-discipline-id")
        disciplines.create(discipline_nome.value, curso_discipline_id.value)
        qtde = len(disciplines.get_all())
        text = f"#Added discipline id: {qtde}, Name: {disciplines.lista(qtde).nome}, Course: {disciplines.get(qtde).curso_id}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def subscribe_course():
    try:
        student_id = Element("student-id")
        curso_id = Element("course-id")
        students.subscribe_in_course(student_id.value, curso_id.value)
        qtde = len(students.get_all())
        text = (
            f"#Student id {qtde} subscribed to course id {students.get(qtde).curso_id}"
        )
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_course():
    try:
        name = Element("course-nome").value
        text = await request(
            f"{BASE_URL}/course",
            "POST",
            json.dumps({"name": name}),
            {"Content-Type": "application/json"},
        )
        __update_terminal(await text.json(), "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_student():
    try:
        name = Element("student-nome").value
        text = await request(
            f"{BASE_URL}/student",
            "POST",
            json.dumps({"name": name}),
            {"Content-Type": "application/json"},
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
