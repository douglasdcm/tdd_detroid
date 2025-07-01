from core.subject import AbstractSubject
from core.student import (
    BasicInformation,
    AbstractStudent,
)
from db_manager import StudentDataManager, SubjectDataManager


class StudentController:
    def add_basic_information(self, nui, name, age) -> None:
        information = BasicInformation(name, age)
        student: AbstractStudent = StudentDataManager().load_by_nui(nui)
        student.add_basic_information(information)
        StudentDataManager().update_object(student)

    def subscribe_to_subject(self, nui, subject_nui) -> None:
        student_dm = StudentDataManager()
        subject_dm = SubjectDataManager()
        student: AbstractStudent = student_dm.load_by_nui(nui)
        subject: AbstractSubject = subject_dm.load_by_nui(subject_nui)
        student.subscribe_to_subject(subject)
        student_dm.update_object(student)
        subject_dm.update_object(subject)

    def list_information(self, nui) -> list:
        return StudentDataManager().load_by_nui(nui)

    def list_subjects(self, nui) -> list:
        student: AbstractStudent = StudentDataManager().load_by_nui(nui)
        return student.list_all_subjects()
