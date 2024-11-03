from src.students import Students
from src.courses import Courses
from src.disciplines import Disciplines
from src.config import conn
from src.utils.utils import inicializa_tabelas
from datetime import datetime
from pyscript import Element, create

inicializa_tabelas(conn)


def subscribe_discipline():
    try:
        aluno_id = int(Element("subscribe-student-id").value)
        materia_id = int(Element("subscribe-discipline-id").value)
        students = Students(conn)
        output = students.inscreve_materia(aluno_id, materia_id)
        text = (
            f"Student id {aluno_id}, Name {students.lista(aluno_id).nome}"
            f" subscribed to discipline id {Disciplines(conn).lista(materia_id).id}"
        )
        __update_terminal(text, "INFO")
        if isinstance(output, str):
            __update_terminal(output, "WARN")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_discipline():
    try:
        discipline_nome = Element("discipline-nome").value
        curso_discipline_id = int(Element("course-discipline-id").value)
        disciplines = Disciplines(conn)
        disciplines.cria(discipline_nome, curso_discipline_id)
        qtde = len(disciplines.lista_tudo())
        text = (
            f"Added discipline id: {qtde}, Name: {disciplines.lista(qtde).nome}"
            f", Course: {disciplines.lista(qtde).curso_id}"
        )
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def subscribe_course():
    try:
        aluno_id = int(Element("student-id").value)
        curso_id = int(Element("course-id").value)
        students = Students(conn)
        students.inscreve_curso(aluno_id, curso_id)
        qtde = len(students.lista_tudo())
        text = (
            f"Student id {qtde} subscribed to course id {students.lista(qtde).curso_id}"
        )
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_course():
    try:
        course_name = Element("course-nome").value
        courses = Courses(conn)
        courses.cria(course_name)
        qtde = len(courses.lista_tudo())
        text = f"Added course id: {qtde}, Nome: {courses.lista(qtde).nome}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def add_student():
    try:
        student_name = Element("student-nome").value
        students = Students(conn)
        students.cria(student_name)
        qtde = len(students.lista_tudo())
        text = f"Added student id: {qtde}, Name: {students.lista(qtde).nome}"
        __update_terminal(text, "INFO")
    except Exception as e:
        __update_terminal(e, "FAIL")


def __update_terminal(text, message_type):
    terminal = Element("local-terminal")
    item = create("pre", classes="py-p")
    item.element.innerText = f"{datetime.now()} {message_type} {text}"
    terminal.element.appendChild(item.element)
    terminal.element.insertBefore(item.element, terminal.element.childNodes[0])
