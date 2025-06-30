from pytest import fixture, raises
from architecture.code_analysis_v3.core.exceptions import InvalidCourse
from architecture.code_analysis_v3.core.subject import SubjectInProgress
from architecture.code_analysis_v3.core.teacher import (
    MaximumSubjectsReached,
    TeacherFull,
    TeacherNotFull,
    TeacherNotWorking,
    TeacherWorking,
)
from architecture.code_analysis_v3.tests.test_core.validator_classes import (
    ValidatorCourse,
    ValidatorSubject,
    ValidatorTeacher,
    ValidatorStudent,
)


@fixture
def teacher():
    yield ValidatorTeacher()


class TestTeacherStateTransition:
    def test_teacher_notworking_when_created(self, teacher: ValidatorTeacher):
        assert isinstance(teacher.state, TeacherNotWorking)

    def test_teacher_subjects_notfull_when_created(self, teacher: ValidatorTeacher):
        assert isinstance(teacher.sub_state, TeacherNotFull)

    def test_teacher_working_when_full_of_subjects(self, teacher: ValidatorTeacher):
        teacher.force_has_maximum_subjects()
        assert isinstance(teacher.state, TeacherWorking)
        assert isinstance(teacher.sub_state, TeacherFull)

    def test_teacher_working_when_with_any_but_not_full_subjects(self, teacher: ValidatorTeacher):
        subject = ValidatorSubject()
        subject.force_state(SubjectInProgress())
        teacher.subscribe_to(subject)
        assert isinstance(teacher.state, TeacherWorking)
        assert isinstance(teacher.sub_state, TeacherNotFull)


class TestTeacherMaximuSubjects:
    def test_teacher_has_not_maximum_subjects_when_created(self, teacher: ValidatorTeacher):
        assert teacher.has_maximum_subjects() is False

    def test_teacher_cannot_exceed_maximum_subjects(self, teacher: ValidatorTeacher):
        teacher.force_has_maximum_subjects()
        with raises(MaximumSubjectsReached):
            teacher.subscribe_to(ValidatorSubject())

    def test_teacher_has_not_maximum_subjects_when_maximum_not_added(
        self, teacher: ValidatorTeacher
    ):
        teacher.subscribe_to(ValidatorSubject())
        assert teacher.has_maximum_subjects() is False

    def test_teacher_has_maximum_subjects_when_maximum_added(self, teacher: ValidatorTeacher):
        for _ in range(3):
            subject = ValidatorSubject()
            subject.force_state(SubjectInProgress())
            teacher.subscribe_to(subject)
        assert teacher.has_maximum_subjects() is True


class TestTeacherInProgressSubject:
    def test_teacher_has_not_inprogress_subjects_when_created(self, teacher: ValidatorTeacher):
        assert teacher.has_inprogress_subject() is False

    def test_teacher_has_not_inprogress_subjects_when_subject_not_inprogress_added(
        self, teacher: ValidatorTeacher
    ):
        subject = ValidatorSubject()
        teacher.subscribe_to(subject)
        assert teacher.has_inprogress_subject() is False

    def test_teacher_has_inprogress_subjects_when_subject_inprogress_added(
        self, teacher: ValidatorTeacher
    ):
        subject = ValidatorSubject()
        subject.force_state(SubjectInProgress())
        teacher.subscribe_to(subject)
        assert teacher.has_inprogress_subject() is True


class TestTeacherSubscribeToSubject:
    def test_teacher_has_not_subjects_when_created(self, teacher: ValidatorTeacher):
        assert len(teacher.list_all_subjects()) == 0

    def test_teacher_has_one_subject_when_subscribe_to_one_subject(self, teacher: ValidatorTeacher):
        teacher.subscribe_to(ValidatorSubject())
        assert len(teacher.list_all_subjects()) == 1

    def test_teacher_has_one_subject_inprogress_when_subscribe_to_one_subject(
        self, teacher: ValidatorTeacher
    ):
        subject = ValidatorSubject()
        subject.force_state(SubjectInProgress())
        teacher.subscribe_to(subject)
        subject2 = ValidatorSubject()
        teacher.subscribe_to(subject2)
        assert len(teacher.list_all_subjects_inprogress()) == 1
        assert len(teacher.list_all_subjects()) == 2


class TestTeacherHasCourse:
    def test_teacher_has_not_course_when_created(self, teacher: ValidatorTeacher):
        assert teacher.has_course() is False

    def test_teacher_has_course_when_course_added(self, teacher: ValidatorTeacher):
        teacher.course = ValidatorCourse()
        assert teacher.has_course() == 1

    def test_teacher_course_no_change_when_defined(self, teacher: ValidatorTeacher):
        course = ValidatorCourse()
        course2 = ValidatorCourse()
        teacher.course = course
        with raises(InvalidCourse):
            teacher.course = course2


class TestTeacherSetGSS:
    def test_teacher_set_gss_when_teacher_working(self, teacher: ValidatorTeacher):

        teacher.set_gss(8, ValidatorStudent(), ValidatorSubject())
