from src.students import Students
from src.courses import Courses
from src.disciplines import Disciplines
from src.config import conn
from datetime import datetime
from pyscript import Element, create
from pyodide.http import pyfetch
import asyncio


async def poc_postgrest():
    response = await pyfetch(url="http://minikube:30501/alunos", method="GET")
    output = f"GET request=> status:{response.status}, json:{await response.json()}"
    __update_terminal(output, "INFO")


def subscribe_discipline():
    try:
        aluno_id = Element("subscribe-student-id")
        materia_id = Element("subscribe-discipline-id")
        students = Students(conn)
        students.inscreve_materia(aluno_id.value, materia_id.value)
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
        students.inscreve_curso(aluno_id.value, curso_id.value)
        qtde = len(students.lista_tudo())
        text = f"#Student id {qtde} subscribed to course id {students.lista(qtde).curso_id}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_course():
    try:
        content = Element("course-nome")
        courses = Courses(conn)
        courses.cria(content.value)
        qtde = len(courses.lista_tudo())
        text = f"#Course id: {qtde}, Nome: {courses.lista(qtde).nome}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


async def add_student():
    try:
        response = await pyfetch(
            url="http://minikube:30501/alunos",
            method="POST",
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
            body={"nome": "any"}
        )
        output = f"GET request=> status:{response.status}, json:{await response.json()}"
        __update_terminal(output, "INFO")
        return
        content = Element("student-nome")
        students = Students(conn)
        students.cria(content.value)
        qtde = len(students.lista_tudo())
        text = f"Added student. id: {qtde}, Name: {students.lista(qtde).nome}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def __update_terminal(text, message_type):
    terminal = Element("local-terminal")
    item = create("pre", classes="py-p")
    item.element.innerText = f"{datetime.now()} {message_type} {text}"
    terminal.element.appendChild(item.element)
    terminal.element.insertBefore(item.element, terminal.element.childNodes[0])
