from sqlalchemy import Column, Integer, String, ForeignKey
from src.utils.sql_client import Base


class MateriaBd(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
