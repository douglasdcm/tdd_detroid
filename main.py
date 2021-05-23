import sys, sqlite3
from src.aluno import Aluno
from src.curso import Curso
from src.materia import Materia
from src.banco_dados import BancoDados

# aluno
cria_aluno = "cria-aluno"
inscreve_aluno_curso = "inscreve-aluno-curso"

# curso
cria_curso = "cria-curso"

def main(*args):
    for argumentos in args:
        if cria_aluno in argumentos:
            if "--nome" in argumentos or "-n" in argumentos:
                try:
                    return _cria_aluno(argumentos[argumentos.index(cria_aluno) + 2])
                except (Exception):
                    raise Exception("Lista de argumentos inválida.")
            else:
                raise Exception("Lista de argumentos inválida.")
        elif inscreve_aluno_curso in argumentos:
            return _inscreve_aluno_curso("aluno", "curso")
        elif cria_curso in argumentos:
            if "--nome" in argumentos or "-n" in argumentos:
                if "--materias" in argumentos or "-m" in argumentos:
                    try:
                        _cria_curso(argumentos[argumentos.index(cria_curso) + 2], 
                                    argumentos[argumentos.index(cria_curso) + 4],
                                    argumentos[argumentos.index(cria_curso) + 5],
                                    argumentos[argumentos.index(cria_curso) + 6])
                    except(Exception):
                        raise Exception("Lista de parâmetros inválida.")
                else:
                    raise Exception("Esperado por parâmetro --materias ou -m.")
            else:
                raise Exception("Esperado por parâmetro --nome ou -n.")
        else:
            raise Exception("Commando inválido.")

def _cria_curso(nome, materia_1, materia_2, materia_3):
    curso = Curso(nome)
    curso.atualiza_materias(Materia(materia_1))
    curso.atualiza_materias(Materia(materia_2))
    curso.atualiza_materias(Materia(materia_3))
    print(f"Curso de {curso.pega_nome()} criado.")

def _inscreve_aluno_curso(aluno, curso):
    print("Aluno inscrito no curso")

def _cria_aluno(nome):
    try:
        aluno = Aluno(nome)
        print(f"Aluno {aluno.pega_nome()} criado com sucesso.")
    except(Exception):
        raise Exception(f"Aluno {nome} não pôde ser criado.")

if __name__ == '__main__':
    main(sys.argv)