from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.utils.sql_client import Base


class CourseDB(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    materia = relationship("MateriaBd")
    aluno = relationship("StudentDB")
