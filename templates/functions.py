from src.sdk.students import Students
from src.courses import Courses
from src.disciplines import Disciplines
from src.config import conn
from datetime import datetime
from pyscript import Element, create
from pyodide.http import pyfetch, FetchResponse
from typing import Optional
import json

# https://github.com/pyscript/pyscript/pull/151/commits/3e3f21c08fa0a5e081804e8fbb11e708ee2813ce
async def request(url:str, method:str = "GET", body:Optional[str] = None,
 headers:Optional[dict[str,str]] = None) -> FetchResponse:
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
    kwargs = {"method":method, "mode":"cors"}
    if body and method not in ["GET", "HEAD"]:
        kwargs["body"] = body
    if headers:
        kwargs["headers"] = headers


    response = await pyfetch(url, **kwargs)
    return response

async def poc_postgrest():
    url = "http://minikube:30501/alunos"
    response = await request(url, "GET")
    # response = await pyfetch(url="http://minikube:30501/alunos", method="GET")
    output = f"GET request=> status:{response.status}, json:{await response.json()}"
    # output = f"GET request=> status:{response}"
    __update_terminal(output, "INFO")


def subscribe_discipline():
    try:
        aluno_id = Element("subscribe-student-id")
        materia_id = Element("subscribe-discipline-id")
        students = Students(conn)
        students.subscribe_in_discipline(aluno_id.value, materia_id.value)
        qtde = len(students.lista_tudo())
        text = f"#Student id {qtde}, Name {students.lista(qtde).nome}, Discipline id {Disciplines(conn).lista(qtde).materia_id}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_discipline():
    try:
        discipline_nome = Element("discipline-nome")
        curso_discipline_id = Element("course-discipline-id")
        disciplines = Disciplines(conn)
        disciplines.cria(discipline_nome.value, curso_discipline_id.value)
        qtde = len(disciplines.lista_tudo())
        text = f"#Added discipline id: {qtde}, Name: {disciplines.lista(qtde).nome}, Course: {disciplines.lista(qtde).curso_id}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def subscribe_course():
    try:
        aluno_id = Element("student-id")
        curso_id = Element("course-id")
        students = Students(conn)
        students.subscribe_in_course(aluno_id.value, curso_id.value)
        qtde = len(students.lista_tudo())
        text = f"#Student id {qtde} subscribed to course id {students.lista(qtde).curso_id}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_course():
    try:
        nome = Element("course-nome").value

        url="http://minikube:30501/alunos"
        response = await request(url, "POST", json.dumps({"nome": nome}), {"Content-Type":"application/json"})
        response = await request(url, "GET")
        output = f"GET request=> status:{response.status}, json:{await response.json()}"
        __update_terminal(output, "INFO")


        content = Element("course-nome")
        courses = Courses(conn)
        courses.cria(content.value)
        qtde = len(courses.lista_tudo())
        text = f"#Course id: {qtde}, Nome: {courses.lista(qtde).nome}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_student():
    try:
        # nome = Element("student-nome").value

        # url="http://minikube:30501/alunos"
        # response = await request(url, "POST", json.dumps({"nome": nome}), {"Content-Type":"application/json"})
        # response = await request(url, "GET")
        # output = f"GET request=> status:{response.status}, json:{await response.json()}"
        # __update_terminal(output, "INFO")
        # return

        content = Element("student-nome").value
        students = Students(conn)
        students.create(content)
        # qtde = len(students.lista_tudo())
        qtde = 42 # fake
        # text = f"Added student. id: {qtde}, Name: {students.lista(qtde).nome}"
        text = f"Added student. id: {qtde}, Name: {content}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def __update_terminal(text, message_type):
    terminal = Element("local-terminal")
    item = create("pre", classes="py-p")
    item.element.innerText = f"{datetime.now()} {message_type} {text}"
    terminal.element.appendChild(item.element)
    terminal.element.insertBefore(item.element, terminal.element.childNodes[0])
