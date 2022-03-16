from enum import Enum


class Situacao(Enum):
    em_curso = "em curso"
    aprovado = "aprovado"
    reprovado = "reprovado"
    trancado = "trancado"
    inexistente = "aluno não matriculado"
    in_progress = "in progress"
    approved = "approved"
    reproved = "reproved"


class SituacaoCurso(Enum):
    cancelado = "cancelado"
