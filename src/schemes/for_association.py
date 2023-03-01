from sqlalchemy import Column, ForeignKey, Integer
from src.utils.sql_client import Base


class MateriaStudentDB(Base):
    __tablename__ = "materia_aluno"

    aluno_nota = Column(Integer)
    discipline_id = Column(ForeignKey("materias.id"), primary_key=True)
    student_id = Column(ForeignKey("alunos.id"), primary_key=True)
