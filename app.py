# -*- coding: utf-8 -*-
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from sys import argv
from sqlite3 import connect as connect
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.materia import Materia
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA
from src.config import database_name
from src.controller.controller import Controller
from src.exceptions.exceptions import (
    ComandoInvalido,
    ListaParametrosInvalida,
)
from src.model.associa_curso_materia import AssociaCursoMateria
from src.model.banco_dados import BancoDados
from src.utils.tables import get_table_list


def main(*args):
    for argumentos in args:
        if "-h" in argumentos or "--help" in argumentos:
            print(
                """
Comandos:
    install
    cria-aluno --nome NOME_ALUNO
    cria-curso --nome NOME_CURSO --materias MATERIA_1 MATERIA_2 MATERIA_3
    inscreve-aluno-curso --curso-id CURSO_ID --aluno-id ALUNO_ID
    atualiza-aluno --aluno-id ID
                    """
            )
            return
        if "cria-aluno" in argumentos:
            _cria_aluno(argumentos)
        elif "inscreve-aluno-curso" in argumentos:
            __inscreve_aluno_curso(argumentos)
        elif "cria-curso" in argumentos:
            __cria_curso(argumentos)
        elif "atualiza-aluno" in argumentos:
            __atualiza_aluno(argumentos)
        elif "cria-materia" in argumentos:
            __cria_materia(argumentos)
        elif "install" in argumentos:
            __install()
        else:
            raise ComandoInvalido("Commando inválido.")


def __install():
    tables = get_table_list()
    database = BancoDados(connect(database_name))
    for table in tables:
        database.deleta_tabela(table["name"])
        database.create_table(table)


def __cria_materia(argumentos):
    nome = "--nome"
    numero_argumentos = 4
    if nome in argumentos and len(argumentos) == numero_argumentos:
        nome = __pega_valor(argumentos, nome)
        materia = Materia(nome)
        bd = connect(database_name)
        Controller(materia, bd).salva()
        print(f"Matéria de {materia.pega_nome()} criada.")
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def __atualiza_aluno(argumentos):
    aluno_id = "--aluno-id"
    situacao = "--situacao"
    nome = "--nome"
    materia = "--materia"
    nota = "--nota"
    try:
        id_ = __pega_valor(argumentos, aluno_id)
        aluno = Aluno()
        bd = connect(database_name)
        Controller(aluno, bd).update(id_)
        if nome in argumentos:
            aluno.define_nome(__pega_valor(argumentos, nome))
            Controller(aluno, bd).update(id_)
        if situacao in argumentos:
            aluno.define_situacao(__pega_valor(argumentos, situacao))
            Controller(aluno, bd).update(id_)
        if materia in argumentos and nota in argumentos:
            aluno.atualiza_materias_cursadas(
                {__pega_valor(argumentos, materia): __pega_valor(argumentos, nota)}
            )
            Controller(aluno, bd).update(id_)

        print(f"Aluno com identificador {id_} atualizado com sucesso.")
    except Exception:
        raise


def __cria_curso(argumentos):
    nome_parametro = "--nome"
    materias_parametro = "--materias"
    numero_argumentos = 8
    if (
        nome_parametro in argumentos
        and materias_parametro in argumentos
        and len(argumentos) == numero_argumentos
    ):
        try:
            nome = __pega_valor(argumentos, nome_parametro)
            materia_1 = __pega_valor(argumentos, materias_parametro)
            materia_2 = __pega_valor(argumentos, materias_parametro, 2)
            materia_3 = __pega_valor(argumentos, materias_parametro, 3)

            bd = connect(database_name)

            course = Curso(nome)
            for materia in [materia_1, materia_2, materia_3]:
                course.atualiza_materias(Materia(materia))
            controller_curso = Controller(course, bd)
            controller_curso.salva()
            curso_obj = controller_curso.get_by_biggest_id()

            for materia in [materia_1, materia_2, materia_3]:
                materia_obj = Controller(Materia(), bd).pega_registro_por_nome(materia)
                Controller(AssociaCursoMateria(curso_obj, materia_obj), bd).salva()
            print(f"Curso de {curso_obj.pega_nome()} criado.")
        except Exception:
            raise
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def __inscreve_aluno_curso(argumentos):
    aluno_parametro = "--aluno-id"
    curso_parametro = "--curso-id"
    numero_parametros = 6
    if (
        aluno_parametro in argumentos
        and curso_parametro in argumentos
        and len(argumentos) == numero_parametros
    ):
        curso_id = __pega_valor(argumentos, curso_parametro)
        aluno_id = __pega_valor(argumentos, aluno_parametro)

        Controller(
            InscricaoAlunoCurso(
                Aluno().define_id(aluno_id), Curso().define_id(curso_id)
            ),
            connect(database_name),
        ).salva()
        print(
            f"Aluno identificado por {aluno_id} inscrito no curso identificado por {curso_id}."
        )
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def _cria_aluno(argumentos):
    nome_parametro = "--nome"
    numero_parametros = 4
    if nome_parametro in argumentos and len(argumentos) == numero_parametros:
        nome = __pega_valor(argumentos, nome_parametro)
        aluno = Aluno(nome)
        bd = connect(database_name)
        controller = Controller(aluno, bd)
        controller.salva()
        print(f"Aluno {nome} criado com sucesso.")
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def __pega_valor(argumentos, parametro, incremento=1):
    return argumentos[argumentos.index(parametro) + incremento]


if __name__ == "__main__":
    main(argv)
