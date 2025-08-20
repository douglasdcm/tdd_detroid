from pytest import fixture
from core.student import StudentInProgress, StudentInitialState
from core.subject import SubjectInProgress, SubjectInitialState
from core.teacher import TeacherNotWorking
from tests.test_core.test_cli.cli_wrapper import StudentCli, TeacherCli
from tests.test_core.test_cli.linux_terminal import LinuxTerminal
from db_manager import StudentDataManager, SubjectDataManager, TeacherDataManager


class TestIntegrationCli:
    _student_dm = StudentDataManager()
    _subject_dm = SubjectDataManager()
    _teacher_dm = TeacherDataManager()
    _cli_student = StudentCli()
    _cli_teacher = TeacherCli()

    def _get_next_nui(self, nuis):
        return list(next(nuis).keys())[0]

    @fixture(autouse=True)
    def init_db(self):
        LinuxTerminal().run("python cli.py init-db")

    def test_student_inprogress_complete(self):
        nuis = self._student_dm.loadall()
        students = []
        for _ in range(3):
            nui = self._get_next_nui(nuis)
            student = self._student_dm.load_by_nui(nui)
            assert isinstance(student.state, StudentInitialState)
            students.append(student)

        nuis = self._teacher_dm.loadall()
        teachers = []
        for _ in range(3):
            nui = self._get_next_nui(nuis)
            teacher = self._teacher_dm.load_by_nui(nui)
            assert isinstance(teacher.state, TeacherNotWorking)
            teachers.append(teacher)

        nuis = self._subject_dm.loadall()
        subjects = []
        for _ in range(3):
            nui = self._get_next_nui(nuis)
            subject = self._subject_dm.load_by_nui(nui)
            assert isinstance(subject.state, SubjectInitialState)
            subjects.append(subject)

        for teacher in teachers:
            for subject in subjects:
                self._cli_teacher.subscribe(teacher.nui, subject.nui)
                self._teacher_dm.save_object(teacher)
                self._subject_dm.save_object(subject)

        for student in students:
            for subject in subjects:
                self._cli_student.subscribe(student.nui, subject.nui)
                self._student_dm.save_object(teacher)
                self._subject_dm.save_object(subject)

        for subject in subjects:
            data = self._subject_dm.load_by_nui(subject.nui)
            assert data.has_course() is True
            assert data.has_teacher() is True
            assert data.has_minimum_inprogress_students() is True
            assert isinstance(data.state, SubjectInProgress)

        for student in students:
            data = self._student_dm.load_by_nui(student.nui)
            for s in data.list_all_subscribed_subjects():
                print(s.state)
            assert data.has_minimum_subjects() is True
            assert data.has_course() is True
            assert isinstance(student.state, StudentInProgress)
