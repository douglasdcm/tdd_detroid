from src.utils import sql_client
from src.controllers.materia import DisciplineController
from src.utils.exceptions import ErroAluno, ErroBancoDados, ErroMateriaAluno
from src.schemes.student import StudentDB
from src.schemes.for_association import MateriaStudentDB
from sqlalchemy.orm import Query
from src.controllers import courses


def update_grade(student_id, materia_id, grade):
    query = Query(MateriaStudentDB).filter(
        MateriaStudentDB.student_id == student_id,
        MateriaStudentDB.materia_id == materia_id,
    )
    mas = sql_client.run_query(query)
    mas[0].aluno_nota = grade
    sql_client.update()


def get_student(student_id):
    try:
        return sql_client.get(StudentDB, student_id)
    except ErroBancoDados:
        raise ErroAluno(f"Aluno {student_id} não existe")


def clear_name(name):
    name = name.strip()
    if len(name) == 0:
        raise ErroAluno("Invalid student name")
    return name


def get_maximum_id():
    return sql_client.list_maximum(StudentDB).id


def get_course_id(student_id):
    curso_id = sql_client.get(StudentDB, student_id).curso_id
    if not curso_id:
        raise ErroAluno(f"Aluno {student_id} não está inscrito em nenhum curso")
    return curso_id


def check_student_already_in_discipline(student_id, materia_id):
    resultado = sql_client.get_all(MateriaStudentDB)
    for instancia in resultado:
        if instancia.student_id == int(student_id) and instancia.materia_id == int(
            materia_id
        ):
            raise ErroMateriaAluno(
                f"Aluno {student_id} já está inscrito na matéria {materia_id}"
            )


def check_student_in_discipline(student_id, materia_id):
    resultado = sql_client.get_all(MateriaStudentDB)
    for instancia in resultado:
        if instancia.student_id == int(student_id) and instancia.materia_id == int(
            materia_id
        ):
            return
    raise ErroAluno(f"Aluno {student_id} não está inscrito na matéria {materia_id}")


def check_grade_boundaries(nota):
    if nota > 10:
        raise ErroAluno("Nota não pode ser maior que 10")
    if nota < 0:
        raise ErroAluno("Nota não pode ser menor que 0")


def __get_disciplines_of_student(student_id):
    query = Query(MateriaStudentDB).filter(
        MateriaStudentDB.student_id == student_id,
    )
    mas = sql_client.run_query(query)
    return mas


def __subscribe_in_discipline(student_id, materia_id):
    ma = MateriaStudentDB(student_id=student_id, materia_id=materia_id)
    sql_client.create(ma)


def __create(nome):
    aluno = StudentDB(nome=nome)
    sql_client.create(aluno)


def calculate_coef_rend(student_id):
    mas = __get_disciplines_of_student(student_id)
    conta = 0
    soma_nota = 0
    for ma in mas:
        if ma.aluno_nota:
            soma_nota += ma.aluno_nota
            conta += 1
    aluno = get_student(student_id)

    aluno.coef_rend = int(round(soma_nota / conta, 1))
    sql_client.update()


def check_student_in_tree_disciplines(student_id):
    resultado = sql_client.get_all(MateriaStudentDB)
    qtde_materias = 0
    for instancia in resultado:
        if instancia.student_id == student_id:
            qtde_materias += 1
        if qtde_materias >= 3:
            return
    raise ErroMateriaAluno("Aluno deve se inscrever em 3 materias no minimo")


def can_subscribe_course(student_id):
    aluno = get_student(student_id)
    if aluno.curso_id is not None:
        raise ErroAluno("Aluno esta inscrito em outro curso")


def __subscribe_in_course(student_id, curso_id):
    courses.check_exists(curso_id)
    student = get_student(student_id)
    student.curso_id = curso_id
    sql_client.update()


def get_all():
    return sql_client.get_all(StudentDB)


def get(id):
    return sql_client.get(StudentDB, id)


def set_grade(student_id, discipline_id, grade):
    grade = int(grade)
    check_grade_boundaries(grade)
    check_student_in_discipline(student_id, discipline_id)
    update_grade(student_id, discipline_id, grade)
    calculate_coef_rend(student_id)


def create(nome):
    nome = clear_name(nome)
    __create(nome)


def subscribe_in_discipline(student_id, materia_id):
    curso_id = get_course_id(student_id)
    DisciplineController().check_exists(materia_id, curso_id)
    check_student_already_in_discipline(student_id, materia_id)
    __subscribe_in_discipline(student_id, materia_id)
    check_student_in_tree_disciplines(student_id)


def subscribe_in_course(student_id, curso_id):
    get_student(student_id)
    can_subscribe_course(student_id)
    __subscribe_in_course(student_id, curso_id)
