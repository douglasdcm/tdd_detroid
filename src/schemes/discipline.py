from sqlalchemy import Column, Integer, String, ForeignKey
from src.utils.sql_client import Base


class MateriaBd(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    curso_id = Column(Integer, ForeignKey("cursos.id"))
