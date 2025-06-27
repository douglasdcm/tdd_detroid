from architecture.code_analysis_v3.core.subject import ISubject
from architecture.code_analysis_v3.core.teacher import AbstractTeacher
from architecture.code_analysis_v3.core.student import BasicInformation, ConcretStudent, IStudent
from architecture.code_analysis_v3.db_manager import StudentDataManager


class StudentController:
    def add_basic_information(self, name, age):
        student = ConcretStudent(name)
        information = BasicInformation(name, age)
        student.add_basic_information(information)
        StudentDataManager().save_object(student)
        print(student.__hash__())

    def list_information(self, nui):
        return StudentDataManager().load_by_nui(nui)
