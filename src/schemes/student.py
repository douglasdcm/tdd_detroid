from sqlalchemy import Column, Integer, String, ForeignKey
from src.utils.sql_client import Base


class AlunoBd(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    coef_rend = Column(Integer)
    curso_id = Column(Integer, ForeignKey("cursos.id"))
