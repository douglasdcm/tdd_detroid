from src.model.university import University
from src.libs.database import Database
from src.model.course import Course
from src.dao.course import CourseDao


class UniversityDao:
    def __init__(self, connection) -> None:
        self.__connection = connection
        self.__table = "university"

    def create(self, university):
        status = university.get_status()
        courses = university.get_courses()
        Database(self.__connection).save(
            self.__table,
            "status",
            "'{}'".format(status),
        )
        for course in courses:
            CourseDao().create(course)
        return True

    def read(self, id_):
        rows = Database(self.__connection).get_by_id(self.__table, id_)[0]
        university = University()
        university.set_status(rows[1])
        query = "select * from courses where university_id = {}".format(id_)
        rows = CourseDao().read(query=query)
        for row in rows:
            course = Course()
            course.set_id(row[0])
            university.add_course(course)
        return university
