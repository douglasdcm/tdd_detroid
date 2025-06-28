from pytest import fixture, raises
from architecture.code_analysis_v3.core.course import Course
from architecture.code_analysis_v3.core.gss import GSS, NoneGSS
from architecture.code_analysis_v3.core.student import (
    StudentApproved,
    BasicInformation,
    AbstractStudent,
    Student,
    StudentInProgress,
    StudentInitialState,
    InvalidStateTransition,
    InvalidSubject,
)
from architecture.code_analysis_v3.core.subject import Subject
from architecture.code_analysis_v3.core.teacher import (
    AbstractTeacher,
    MaximumSubjectsReached,
    Teacher,
    TeacherFull,
    TeacherNotFull,
    TeacherNotWorking,
    TeacherWorking,
)
from architecture.code_analysis_v3.tests.test_core.test_constants import ANY_NAME


@fixture
def teacher():
    yield Teacher(ANY_NAME)


class TestTeacherStateTransition:
    def test_teacher_notworking_when_created(self, teacher: AbstractTeacher):
        assert isinstance(teacher.state, TeacherNotWorking)

    def test_teacher_subjects_notfull_when_created(self, teacher: AbstractTeacher):
        assert isinstance(teacher.sub_state, TeacherNotFull)

    def test_teacher_working_when_full_of_subjects(self, teacher: AbstractTeacher):
        teacher.subscribe_to(Subject(ANY_NAME))
        teacher.subscribe_to(Subject(ANY_NAME))
        teacher.subscribe_to(Subject(ANY_NAME))
        assert isinstance(teacher.state, TeacherWorking)
        assert isinstance(teacher.sub_state, TeacherFull)

    def test_teacher_working_when_with_any_but_not_full_subjects(self, teacher: AbstractTeacher):
        teacher.subscribe_to(Subject(ANY_NAME))
        assert isinstance(teacher.state, TeacherWorking)
        assert isinstance(teacher.sub_state, TeacherNotFull)


class TestTeacherMaximuSubjects:
    def test_teacher_cannot_exceed_maximum_subjects(self, teacher: AbstractTeacher):
        teacher.subscribe_to(Subject(ANY_NAME))
        teacher.subscribe_to(Subject(ANY_NAME))
        teacher.subscribe_to(Subject(ANY_NAME))
        # exceeded
        with raises(MaximumSubjectsReached):
            teacher.subscribe_to(Subject(ANY_NAME))


class TestTeacherSetGSS:
    def test_notify_student_when_teacher_set_gss(self, teacher: AbstractTeacher):
        course = Course(ANY_NAME)
        subject = Subject(ANY_NAME)
        subject.course = course
        student = Student(ANY_NAME)
        student.course = course
        student.subscribe_to_subject(subject)
        teacher.subscribe_to(subject)
        teacher.set_gss(8, student, subject)
        assert len(student._grades) == 1
