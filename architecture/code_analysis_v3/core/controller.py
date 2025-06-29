from architecture.code_analysis_v3.core.subject import AbstractSubject
from architecture.code_analysis_v3.core.student import (
    BasicInformation,
    AbstractStudent,
)
from architecture.code_analysis_v3.db_manager import StudentDataManager, SubjectDataManager


class StudentController:
    def add_basic_information(self, nui, name, age) -> None:
        information = BasicInformation(name, age)
        student: AbstractStudent = StudentDataManager().load_by_nui(nui)
        student.add_basic_information(information)
        StudentDataManager().update_object(student)

    def subscribe_to_subject(self, nui, subject_nui) -> None:
        student: AbstractStudent = StudentDataManager().load_by_nui(nui)
        subject: AbstractSubject = SubjectDataManager().load_by_nui(subject_nui)
        return student.subscribe_to_subject(subject)

    def list_information(self, nui) -> list:
        return StudentDataManager().load_by_nui(nui)

    def list_subjects(self, nui) -> list:
        student: AbstractStudent = StudentDataManager().load_by_nui(nui)
        return student.list_all_subjects()
