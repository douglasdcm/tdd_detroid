from sqlalchemy import Column, ForeignKey
from src.utils.sql_client import Base


class MateriaAlunoBd(Base):
    __tablename__ = "materia_aluno"
    materia_id = Column(ForeignKey("materias.id"), primary_key=True)
    aluno_id = Column(ForeignKey("alunos.id"), primary_key=True)
