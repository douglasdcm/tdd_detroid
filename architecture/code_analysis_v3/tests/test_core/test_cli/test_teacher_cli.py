from pytest import fixture
from tests.test_core.test_cli.cli_wrapper import TeacherCli
from tests.test_core.test_cli.linux_terminal import LinuxTerminal
from db_manager import TeacherDataManager, SubjectDataManager


class TestTeacherCli:
    _teacher_dm = TeacherDataManager()
    _subject_dm = SubjectDataManager()
    _cli = TeacherCli()

    def _get_nui_by_index(self, nuis, index=0):
        return list(next(nuis).keys())[index]

    @fixture(autouse=True)
    def init_db(self):
        LinuxTerminal().run("python cli.py init-db")

    @fixture
    def nui(self):
        nuis = self._teacher_dm.loadall()
        yield self._get_nui_by_index(nuis)

    @fixture
    def snui(self):
        nuis = self._subject_dm.loadall()
        yield self._get_nui_by_index(nuis)

    def test_teacher_add_information(self, nui):
        name = "any"
        age = 42
        self._cli.add_info(nui, name, age)
        assert self._teacher_dm.load_by_nui(nui).name == name
        assert self._teacher_dm.load_by_nui(nui).age == age
        actual = self._cli.list_information(nui)
        assert nui in actual

    def test_teacher_subscribe(self, nui, snui):
        teacher = self._teacher_dm.load_by_nui(nui)
        subject = self._subject_dm.load_by_nui(snui)
        assert teacher.course.nui == subject.course.nui

        self._teacher_dm.update_object(teacher)
        self._subject_dm.update_object(subject)
        teacher = self._teacher_dm.load_by_nui(nui)
        subject = self._subject_dm.load_by_nui(snui)
        assert teacher.course.nui == subject.course.nui
        assert teacher.list_all_subjects() == []

        self._cli.subscribe(nui, snui)
        assert subject.nui in [s.nui for s in self._teacher_dm.load_by_nui(nui).list_all_subjects()]
        actual = self._cli.list_subjects(nui)
        assert "Subject NUI" in actual
