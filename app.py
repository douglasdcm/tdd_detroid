# -*- coding: utf-8 -*-
from typing import no_type_check_decorator
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from sys import argv
from sqlite3 import connect
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.materia import Materia
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA
from src.config import banco_dados
from src.controller.controller import Controller
from src.exceptions.exceptions import ComandoInvalido, ListaParametrosInvalida, MateriaInvalida, \
    MateriaInvalida
from src.model.associa_curso_materia import AssociaCursoMateria

first = 0

# banco de dados
bd = connect(banco_dados)

# aluno
cria_aluno = "cria-aluno"
inscreve_aluno_curso = "inscreve-aluno-curso"
atualiza_aluno = "atualiza-aluno"

# curso
cria_curso = "cria-curso"

# matéria
cria_materia = "cria-materia"


def main(*args):
    for argumentos in args:
        if "-h" in argumentos or "--help" in argumentos:
            print("""
Comandos:
    cria-aluno --nome NOME_ALUNO
    cria-curso --nome NOME_CURSO --materias MATERIA_1 MATERIA_2 MATERIA_3
    inscreve-aluno-curso --curso-id CURSO_ID --aluno-id ALUNO_ID
    atualiza-aluno --aluno-id ID
                    """)
            return
        if cria_aluno in argumentos:
            _cria_aluno(argumentos)
        elif inscreve_aluno_curso in argumentos:
            _inscreve_aluno_curso(argumentos)
        elif cria_curso in argumentos:
            _cria_curso(argumentos)
        elif atualiza_aluno in argumentos:
            _atualiza_aluno(argumentos)
        elif cria_materia in argumentos:
            _cria_materia(argumentos)
        else:
            raise ComandoInvalido("Commando inválido.")


def _cria_materia(argumentos):
    nome = "--nome"
    numero_argumentos = 4
    if nome in argumentos and len(argumentos) == numero_argumentos:
        nome = _pega_valor(argumentos, nome)
        materia = Materia(nome)
        Controller(materia, bd).salva()
        print(f"Matéria de {materia.pega_nome()} criada.")
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def _atualiza_aluno(argumentos):
    aluno_id = "--aluno-id"
    situacao = "--situacao"
    nome = "--nome"
    materia = "--materia"
    nota = "--nota"
    aluno = Aluno()
    try:
        if aluno_id in argumentos:
            id_ = _pega_valor(argumentos, aluno_id)
            Controller(aluno, bd).atualiza(id_)
        if nome in argumentos:
            nome_ = _pega_valor(argumentos, nome)
            aluno.define_nome(nome_)
            Controller(aluno, bd).atualiza(id_)
        if situacao in argumentos:
            situacao_ = _pega_valor(argumentos, situacao)
            aluno.define_situacao(situacao_)
            Controller(aluno, bd).atualiza(id_)
        if materia in argumentos and nota in argumentos:
            materia_ = _pega_valor(argumentos, materia)
            nota_ = _pega_valor(argumentos, nota)
            materias = {materia_: nota_}
            aluno.atualiza_materias_cursadas(materias)
            Controller(aluno, bd).atualiza(id_)

        print(f"Aluno com identificador {id_} atualizado com sucesso.")
    except Exception:
        raise


def _cria_curso(argumentos):
    nome_parametro = "--nome"
    materias_parametro = "--materias"
    numero_argumentos = 8
    if nome_parametro in argumentos and materias_parametro in argumentos \
            and len(argumentos) == numero_argumentos:
        try:
            nome = _pega_valor(argumentos, nome_parametro)
            materia_1 = _pega_valor(argumentos, materias_parametro)
            materia_2 = _pega_valor(argumentos, materias_parametro, 2)
            materia_3 = _pega_valor(argumentos, materias_parametro, 3)

            curso = Curso(nome)
            controller_curso = Controller(curso, bd)
            controller_curso.salva()
            registro = controller_curso.pega_registro_por_nome(nome)
            curso_id = registro.pega_id()
            curso.define_id(curso_id)

            controller = Controller(Materia(None), bd)
            for materia in [materia_1, materia_2, materia_3]:
                registro = controller.pega_registro_por_nome(materia)
                materia_id = registro.pega_id()
                materia = Materia(materia)
                materia.define_id(materia_id)
                curso.atualiza_materias(materia)

                Controller(AssociaCursoMateria(curso, materia), bd).salva()
            print(f"Curso de {curso.pega_nome()} criado.")
        except Exception:
            raise
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def _inscreve_aluno_curso(argumentos):
    aluno_parametro = "--aluno-id"
    curso_parametro = "--curso-id"
    numero_parametros = 6
    if aluno_parametro in argumentos and curso_parametro in argumentos \
            and len(argumentos) == numero_parametros:
        curso_id = _pega_valor(argumentos, curso_parametro)
        aluno_id = _pega_valor(argumentos, aluno_parametro)
        inscricao = InscricaoAlunoCurso(aluno_id, curso_id)
        Controller(inscricao, bd).salva()
        print(f"Aluno identificado por {aluno_id} inscrito no curso identificado por {curso_id}.")
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def _cria_aluno(argumentos):
    nome_parametro = "--nome"
    numero_parametros = 4
    if nome_parametro in argumentos and len(argumentos) == numero_parametros:
        nome = _pega_valor(argumentos, nome_parametro)
        aluno = Aluno(nome)
        controller = Controller(aluno, bd)
        controller.salva()
        print(f"Aluno {nome} criado com sucesso.")
    else:
        raise ListaParametrosInvalida(LISTA_PARAMETROS_INVALIDA)


def _pega_valor(argumentos, parametro, incremento=1):
    return argumentos[argumentos.index(parametro) + incremento]


if __name__ == '__main__':
    main(argv)
