from src.controllers import courses as controller


def create(nome):
    controller.create(nome)


def get_all():
    return controller.get_all()


def get(id_):
    return controller.get(id_)
