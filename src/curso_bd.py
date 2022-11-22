from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.sql_client import Base


class CursoBd(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    materia = relationship("Materia")
    aluno = relationship("Aluno")
