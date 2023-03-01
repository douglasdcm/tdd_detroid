from src.utils import sql_client
from src.controllers import disciplines
from src.utils.exceptions import ErrorStudent, ErrorDatabase, ErrorInvalidInteger
from src.schemes.student import StudentDB
from src.schemes.for_association import MateriaStudentDB
from sqlalchemy.orm import Query
from src.controllers import courses
from src.utils.utils import convert_id_to_integer


def update_grade(student_id, discipline_id, grade):
    query = Query(MateriaStudentDB).filter(
        MateriaStudentDB.student_id == student_id,
        MateriaStudentDB.discipline_id == discipline_id,
    )
    mas = sql_client.run_query(query)
    mas[0].aluno_nota = grade
    sql_client.update()


def get_student(student_id):
    try:
        return sql_client.get(StudentDB, student_id)
    except ErrorDatabase:
        raise ErrorStudent(f"Aluno {student_id} não existe")


def clear_name(name):
    name = name.strip()
    if len(name) == 0:
        raise ErrorStudent("Invalid student name")
    return name


def get_maximum_id():
    return sql_client.get_maximum(StudentDB).id


def get_course_id(student_id):
    course_id = sql_client.get(StudentDB, student_id).course_id
    if not course_id:
        raise ErrorStudent(f"Aluno {student_id} não está inscrito em nenhum course")
    return course_id


def check_student_already_in_discipline(student_id, discipline_id):
    resultado = sql_client.get_all(MateriaStudentDB)
    for instancia in resultado:
        if instancia.student_id == int(student_id) and instancia.discipline_id == int(
            discipline_id
        ):
            raise ErrorStudent(
                f"Aluno {student_id} já está inscrito na matéria {discipline_id}"
            )


def check_student_in_discipline(student_id, discipline_id):
    resultado = sql_client.get_all(MateriaStudentDB)
    for instancia in resultado:
        if instancia.student_id == int(student_id) and instancia.discipline_id == int(
            discipline_id
        ):
            return
    raise ErrorStudent(f"Aluno {student_id} não está inscrito na matéria {discipline_id}")


def check_grade_boundaries(nota):
    if nota > 10:
        raise ErrorStudent("Nota não pode ser maior que 10")
    if nota < 0:
        raise ErrorStudent("Nota não pode ser menor que 0")


def __get_disciplines_of_student(student_id):
    query = Query(MateriaStudentDB).filter(
        MateriaStudentDB.student_id == student_id,
    )
    mas = sql_client.run_query(query)
    return mas


def __subscribe_in_discipline(student_id, discipline_id):
    ma = MateriaStudentDB(student_id=student_id, discipline_id=discipline_id)
    sql_client.create(ma)


def __create(name):
    aluno = StudentDB(name=name)
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
    raise ErrorStudent("Aluno deve se inscrever em 3 materias no minimo")


def can_subscribe_course(student_id):
    aluno = get_student(student_id)
    if aluno.course_id is not None:
        raise ErrorStudent("Aluno esta inscrito em outro course")


def __subscribe_in_course(student_id, course_id):
    courses.check_exists(course_id)
    student = get_student(student_id)
    student.course_id = course_id
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


def create(name):
    name = clear_name(name)
    __create(name)


def subscribe_in_discipline(student_id, discipline_id):
    try:
        student_id = convert_id_to_integer(student_id)
    except ErrorInvalidInteger:
        raise ErrorStudent("The student id is not a valid integer")
    try:
        discipline_id = convert_id_to_integer(discipline_id)
    except ErrorInvalidInteger:
        raise ErrorStudent("The discipline id is not a valid integer")
    course_id = get_course_id(student_id)
    disciplines.check_exists(discipline_id, course_id)
    check_student_already_in_discipline(student_id, discipline_id)
    __subscribe_in_discipline(student_id, discipline_id)
    check_student_in_tree_disciplines(student_id)


def subscribe_in_course(student_id, course_id):
    try:
        student_id = convert_id_to_integer(student_id)
    except ErrorInvalidInteger:
        raise ErrorStudent("The student id is not a valid integer")
    try:
        course_id = convert_id_to_integer(course_id)
    except ErrorInvalidInteger:
        raise ErrorStudent("The course id is not a valid integer")
    get_student(student_id)
    can_subscribe_course(student_id)
    __subscribe_in_course(student_id, course_id)
