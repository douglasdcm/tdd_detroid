from enum import Enum


class Situacao(Enum):
    em_curso = "em curso"
    aprovado = "aprovado"
    reprovado = "reprovado"
    trancado = "trancado"
    inexistente = "aluno inexistente"
