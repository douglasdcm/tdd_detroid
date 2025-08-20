from pytest import fixture
from tests.test_core.test_cli.cli_wrapper import StudentCli
from tests.test_core.test_cli.linux_terminal import LinuxTerminal
from db_manager import StudentDataManager, SubjectDataManager, TeacherDataManager


class TestStudentCli:
    _student_dm = StudentDataManager()
    _subject_dm = SubjectDataManager()
    _teacher_dm = TeacherDataManager()
    _cli_student = StudentCli()

    def _get_next_nui(self, nuis):
        return list(next(nuis).keys())[0]

    @fixture(autouse=True)
    def init_db(self):
        LinuxTerminal().run("python cli.py init-db")

    @fixture
    def nui(self):
        nuis = self._student_dm.loadall()
        yield self._get_next_nui(nuis)

    @fixture
    def snui(self):
        nuis = self._subject_dm.loadall()
        yield self._get_next_nui(nuis)

    def test_student_add_information(self, nui):
        name = "any"
        age = 42
        self._cli_student.add_info(nui, name, age)
        assert self._student_dm.load_by_nui(nui).name == name
        assert self._student_dm.load_by_nui(nui).age == age
        actual = self._cli_student.list_information(nui)
        assert nui in actual

    def test_student_subscribe(self, nui, snui):
        student = self._student_dm.load_by_nui(nui)
        subject = self._subject_dm.load_by_nui(snui)
        assert student.course.nui == subject.course.nui

        self._student_dm.update_object(student)
        self._subject_dm.update_object(subject)
        student = self._student_dm.load_by_nui(nui)
        subject = self._subject_dm.load_by_nui(snui)
        assert student.course.nui == subject.course.nui
        assert student.list_all_subscribed_subjects() == []

        self._cli_student.subscribe(nui, snui)
        assert subject.nui in [
            s.nui for s in self._student_dm.load_by_nui(nui).list_all_subscribed_subjects()
        ]
        actual = self._cli_student.list_subjects(nui)
        assert "Subject NUI" in actual
