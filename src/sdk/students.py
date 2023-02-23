from src.controllers import students as controller


def set_grade(student_id, materia_id, nota):
    controller.set_grade(student_id, materia_id, nota)


def subscribe_in_course(student_id, curso_id):
    controller.subscribe_in_course(student_id, curso_id)


def subscribe_in_discipline(student_id, materia_id):
    controller.subscribe_in_discipline(student_id, materia_id)


def create(nome):
    controller.create(nome)


def get_all():
    return controller.get_all()


def get(id_):
    return controller.get(id_)
