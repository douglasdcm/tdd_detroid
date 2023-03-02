from sqlalchemy import Column, Integer, String, ForeignKey, Float
from src.utils.sql_client import Base


class StudentDB(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    coef_rend = Column(Float)
    course_id = Column(Integer, ForeignKey("courses.id"))
