from core.subject import AbstractSubject
from core.student import (
    BasicInformation,
    AbstractStudent,
)
from core.teacher import AbstractTeacher
from db_manager import StudentDataManager, SubjectDataManager, TeacherDataManager


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


class TeacherController:
    def add_basic_information(self, nui, name, age) -> None:
        information = BasicInformation(name, age)
        teacher: AbstractTeacher = TeacherDataManager().load_by_nui(nui)
        teacher.add_basic_information(information)
        TeacherDataManager().update_object(teacher)

    def subscribe_to_subject(self, nui, subject_nui) -> None:
        teacher_dm = TeacherDataManager()
        subject_dm = SubjectDataManager()
        teacher: AbstractTeacher = teacher_dm.load_by_nui(nui)
        subject: AbstractSubject = subject_dm.load_by_nui(subject_nui)
        teacher.subscribe_to(subject)
        teacher_dm.update_object(teacher)
        subject_dm.update_object(subject)

    def list_information(self, nui) -> BasicInformation:
        return TeacherDataManager().load_by_nui(nui)

    def list_subjects(self, nui) -> list[AbstractSubject]:
        teacher: AbstractTeacher = TeacherDataManager().load_by_nui(nui)
        return teacher.list_all_subjects()
