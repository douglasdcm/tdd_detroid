# -*- coding: utf-8 -*-
import sys, sqlite3
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.materia import Materia
from src.dao.dao_fabrica import DaoFabrica
from src.utils.messagens import LISTA_PARAMETROS_INVALIDA

# banco de dados
bd = sqlite3.connect("sample.db")

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
        dao = DaoFabrica(curso, bd)
        dao.fabrica_objetos_dao().salva()
        print(f"Curso de {curso.pega_nome()} criado.")
    else:
        raise Exception(LISTA_PARAMETROS_INVALIDA)


def _inscreve_aluno_curso(argumentos):
    aluno_parametro = "--aluno"
    curso_parametro = "--curso"
    numero_parametros = 6
    if aluno_parametro in argumentos \
        and curso_parametro in argumentos \
        and len(argumentos) == numero_parametros:
        curso = _pega_valor(argumentos, curso_parametro)
        aluno = _pega_valor(argumentos, aluno_parametro)
        curso = Curso(curso)
        aluno = Aluno(aluno)
        curso.adiciona_aluno(aluno)
        print(f"Aluno {aluno.pega_nome()} inscrito no curso de {curso.pega_nome()}.")
    else:
        raise Exception(LISTA_PARAMETROS_INVALIDA)

def _cria_aluno(argumentos):
    nome_parametro = "--nome"
    numero_parametros = 4
    if nome_parametro in argumentos \
        and len(argumentos) == numero_parametros:
        nome = _pega_valor(argumentos, nome_parametro)
        aluno = Aluno(nome)
        dao = DaoFabrica(aluno, bd)
        dao.fabrica_objetos_dao().salva()
        print(f"Aluno {aluno.pega_nome()} criado com sucesso.")
    else:
        raise Exception(LISTA_PARAMETROS_INVALIDA)

def _pega_valor(argumentos, parametro, incremento = 1):
    return argumentos[argumentos.index(parametro) + incremento]

if __name__ == '__main__':
    main(sys.argv)