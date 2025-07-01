from pytest import fixture
from core.spy_logger import spy_logger
from tests.test_cli.linux_terminal import LinuxTerminal
from db_manager import StudentDataManager, SubjectDataManager
from tests.test_core.validator_classes import ValidatorCourse


class StudentCli(LinuxTerminal):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    @spy_logger
    def add_info(self, nui, name, age):
        self.call(f"python cli.py student add-info --nui {nui} --name {name} --age {age}")

    @spy_logger
    def subscribe(self, nui, snui):
        self.call(f"python cli.py student subscribe --nui {nui} --snui {snui}")


class TestStudentCli:
    _student_dm = StudentDataManager()
    _subject_dm = SubjectDataManager()
    _cli = StudentCli()

    def _get_nui_by_index(self, nuis, index=0):
        return list(next(nuis).keys())[index]

    @fixture(autouse=True)
    def init_db(self):
        LinuxTerminal().call("python cli.py init-db")

    @fixture
    def nui(self):
        nuis = self._student_dm.loadall()
        yield self._get_nui_by_index(nuis)

    @fixture
    def snui(self):
        nuis = self._subject_dm.loadall()
        yield self._get_nui_by_index(nuis)

    def test_student_add_information(self, nui):
        name = "any"
        age = 42
        self._cli.add_info(nui, name, age)
        assert self._student_dm.load_by_nui(nui).name == name
        assert self._student_dm.load_by_nui(nui).age == age

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

        self._cli.subscribe(nui, snui)
        assert subject.nui in [
            s.nui for s in self._student_dm.load_by_nui(nui).list_all_subscribed_subjects()
        ]
