from src.students import Students
from src.courses import Courses
from src.disciplines import Disciplines
from src.config import conn
from src.utils.utils import inicializa_tabelas
from pyscript import Element

inicializa_tabelas(conn)


def inscreve_materia():
    try:
        aluno_id = Element("inscreve-aluno-id")
        materia_id = Element("inscreve-materia-id")
        students = Students(conn)
        students.inscreve_materia(aluno_id.value, materia_id.value)
        qtde = len(students.lista_tudo())
        print(
            "#Aluno",
            qtde,
            " Nome ",
            students.lista(qtde).nome,
            " Materia ",
            Disciplines(conn).lista(qtde).materia_id,
        )
    except Exception as e:
        print(e)


def add_materia():
    try:
        materia_nome = Element("materia-nome")
        curso_materia_id = Element("curso-materia-id")
        disciplines = Disciplines(conn)
        disciplines.cria(materia_nome.value, curso_materia_id.value)
        qtde = len(disciplines.lista_tudo())
        print(
            "#Materia",
            qtde,
            " Nome ",
            disciplines.lista(qtde).nome,
            " Curso ",
            disciplines.lista(qtde).curso_id,
        )
    except Exception as e:
        print(e)


def inscreve_curso():
    try:
        aluno_id = Element("aluno-id")
        curso_id = Element("curso-id")
        students = Students(conn)
        students.inscreve_curso(aluno_id.value, curso_id.value)
        qtde = len(students.lista_tudo())
        print("#Aluno", qtde, " Curso ", students.lista(qtde).curso_id)
    except Exception as e:
        print(e)


def add_curso():
    try:
        content = Element("curso-nome")
        courses = Courses(conn)
        courses.cria(content.value)
        qtde = len(courses.lista_tudo())
        print("#Curso", qtde, " Nome ", courses.lista(qtde).nome)
    except Exception as e:
        print(e)


def add_aluno():
    try:
        content = Element("aluno-nome")
        students = Students(conn)
        students.cria(content.value)
        qtde = len(students.lista_tudo())
        print("#Aluno", qtde, " Nome ", students.lista(qtde).nome)
    except Exception as e:
        print(e)
