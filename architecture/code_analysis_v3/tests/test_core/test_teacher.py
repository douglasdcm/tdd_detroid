from pytest import fixture, raises
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
    def test_teacher_cannot_exceed_maximum_subjects(self, teacher: ValidatorTeacher):
        teacher.force_has_maximum_subjects()
        # exceeded
        with raises(MaximumSubjectsReached):
            teacher.subscribe_to(ValidatorSubject())


class TestTeacherSetGSS:
    def test_notify_student_when_teacher_sets_gss(self, teacher: ValidatorTeacher):
        course = ValidatorCourse()
        subject = ValidatorSubject()
        subject.course = course
        student = ValidatorStudent()
        student.course = course
        student.subscribe_to_subject(subject)
        teacher.subscribe_to(subject)
        teacher.set_gss(8, student, subject)
        assert len(student.grades) == 1
