from sqlalchemy import Column, ForeignKey, Integer
from src.utils.sql_client import Base


class MateriaAlunoBd(Base):
    __tablename__ = "materia_aluno"

    id = Column(Integer, primary_key=True)
    aluno_nota = Column(Integer)
    materia_id = Column(ForeignKey("materias.id"))
    aluno_id = Column(ForeignKey("alunos.id"))
