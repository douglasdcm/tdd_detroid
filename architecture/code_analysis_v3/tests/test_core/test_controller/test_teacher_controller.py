from pytest import fixture
from core.controller import TeacherController
from db_manager import SubjectDataManager, TeacherDataManager
from tests.test_core.test_cli.linux_terminal import LinuxTerminal


class TestTeacherController:
    _student_dm = TeacherDataManager()
    _subject_dm = SubjectDataManager()

    def _get_nui_by_index(self, nuis, index=0):
        return list(next(nuis).keys())[index]

    @fixture(autouse=True)
    def init_db(self):
        LinuxTerminal().run("python cli.py init-db")

    @fixture
    def nui(self):
        nuis = self._student_dm.loadall()
        yield self._get_nui_by_index(nuis)

    @fixture
    def snui(self):
        nuis = self._subject_dm.loadall()
        yield self._get_nui_by_index(nuis)

    @fixture
    def controller(self):
        yield TeacherController()

    def test_teacher_add_information(self, controller: TeacherController, nui):
        name = "any"
        age = 42
        controller.add_basic_information(nui, name, age)
        actual = controller.list_information(nui)
        assert actual.name == name

    def test_teacher_subscribe(self, controller: TeacherController, nui, snui):
        controller.subscribe_to_subject(nui, subject_nui=snui)
        actual = controller.list_subjects(nui)[0]
        assert actual.has_teacher() is True
        assert actual.teacher.nui == int(nui)
