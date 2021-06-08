# -*- coding: utf-8 -*-
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from sys import argv
from sqlite3 import connect
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.materia import Materia
from src.dao.dao_fabrica import DaoFabrica
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA
from src.config import banco_dados
from src.controller.controller import Controller

first = 0

# banco de dados
bd = connect(banco_dados)

# aluno
cria_aluno = "cria-aluno"
inscreve_aluno_curso = "inscreve-aluno-curso"

# curso
cria_curso = "cria-curso"

def main(*args):
    for argumentos in args:
        if cria_aluno in argumentos:
            _cria_aluno(argumentos) 
        elif inscreve_aluno_curso in argumentos:
            _inscreve_aluno_curso(argumentos)
        elif cria_curso in argumentos:
            _cria_curso(argumentos)
        else:
            raise Exception("Commando inválido.")

def _cria_curso(argumentos):
    nome_parametro = "--nome"
    materias_parametro = "--materias"
    numero_argumentos = 8
    if nome_parametro in argumentos \
        and materias_parametro in argumentos \
        and len(argumentos) == numero_argumentos:
        nome = _pega_valor(argumentos, nome_parametro)
        materia_1 = _pega_valor(argumentos, materias_parametro)
        materia_2 = _pega_valor(argumentos, materias_parametro, 2)
        materia_3 = _pega_valor(argumentos, materias_parametro, 3)
        curso = Curso(nome) 
        curso.atualiza_materias(Materia(materia_1))
        curso.atualiza_materias(Materia(materia_2))
        curso.atualiza_materias(Materia(materia_3))
        Controller(curso, bd).salva()
        print(f"Curso de {curso.pega_nome()} criado.")
    else:
        raise Exception(LISTA_PARAMETROS_INVALIDA)


def _inscreve_aluno_curso(argumentos):
    aluno_parametro = "--aluno-id"
    curso_parametro = "--curso-id"
    numero_parametros = 6
    if aluno_parametro in argumentos \
        and curso_parametro in argumentos \
        and len(argumentos) == numero_parametros:
        curso_id = _pega_valor(argumentos, curso_parametro)
        aluno_id = _pega_valor(argumentos, aluno_parametro)
        inscricao = InscricaoAlunoCurso(aluno_id, curso_id)
        Controller(inscricao, bd).salva()
        print(f"Aluno identificado por {aluno_id} inscrito no curso identificado por {curso_id}.")
    else:
        raise Exception(LISTA_PARAMETROS_INVALIDA)

def _cria_aluno(argumentos):
    nome_parametro = "--nome"
    numero_parametros = 4
    if nome_parametro in argumentos \
        and len(argumentos) == numero_parametros:
        nome = _pega_valor(argumentos, nome_parametro)
        aluno = Aluno(nome)
        controller = Controller(aluno, bd)
        controller.salva()
        print(f"Aluno {nome} criado com sucesso.")
    else:
        raise Exception(LISTA_PARAMETROS_INVALIDA)

def _pega_valor(argumentos, parametro, incremento = 1):
    return argumentos[argumentos.index(parametro) + incremento]

if __name__ == '__main__':
    main(argv)