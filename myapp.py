from src.aluno import Aluno

aluno = Aluno()
print(aluno.pega_coeficiente_rendimento())

materias = {"mat": 8}
aluno.atualiza_materias_cursadas(materias)
print(aluno.pega_coeficiente_rendimento())

aluno.calcula_situacao()
print(aluno.pega_situacao())

materias = {"hist": 8, "geo": 8}
aluno.calcula_situacao()
print(aluno.pega_situacao())

