import logging
from pytest import raises
from core.course import NoneCourse
from core.exceptions import InvalidCourse
from core.student import (
    StudentInProgress,
)
from core.subject import SubjectInProgress, SubjectInitialState
from tests.test_core.validator_classes import (
    ValidatorCourse,
    ValidatorStudent,
    ValidatorSubject,
    ValidatorTeacher,
)


class TestSubjectStateTransition:
    def test_subject_in_initial_state_when_created(self):
        subject = ValidatorSubject()
        assert isinstance(subject.state, SubjectInitialState)

    def test_subject_in_initial_State_when_has_course_teacher_and_no_minimum_inprogress_students(
        self,
    ):
        subject = ValidatorSubject()
        subject.force_has_course()
        subject.force_has_teacher()
        assert isinstance(subject.state, SubjectInitialState)

    def test_subject_inprogress_when_has_course_no_teacher_and_no_minimum_inprogress_students(self):
        subject = ValidatorSubject()
        subject.force_has_course()
        assert isinstance(subject.state, SubjectInitialState)

    def test_subject_inprogress_when_has_course_teacher_and_minimum_inprogress_students(self):
        subject = ValidatorSubject()
        subject.force_has_course()
        subject.force_has_teacher()
        subject.force_has_minimum_in_progress_students()
        assert isinstance(subject.state, SubjectInProgress)

    def test_subject_state_not_change_when_inprogress(self):
        subject = ValidatorSubject()
        subject.force_has_course()
        subject.force_has_teacher()
        subject.force_has_minimum_in_progress_students()
        assert isinstance(subject.state, SubjectInProgress)
        assert isinstance(subject.state, SubjectInProgress)


class TestSubjectHasCourse:
    def test_subject_has_no_course_when_created(self):
        subject = ValidatorSubject()
        assert subject.has_course() is False

    def test_subject_has_course_when_course_added(self):
        subject = ValidatorSubject()
        subject.course = ValidatorCourse()
        assert subject.has_course() is True


class TestSubjectCourse:
    def test_subject_course_not_defined_when_created(self):
        subject = ValidatorSubject()
        assert isinstance(subject.course, NoneCourse)

    def test_subject_course_no_change_when_defined(self):
        subject = ValidatorSubject()
        course = ValidatorCourse()
        subject.course = course
        assert subject.course == course
        course2 = ValidatorCourse()
        with raises(InvalidCourse):
            subject.course = course2


class TestSubjectHasTeacher:
    def test_subject_has_no_teacher_when_created(self):
        subject = ValidatorSubject()
        assert subject.has_teacher() is False

    def test_subject_has_teacher_when_teacher_added(self):
        subject = ValidatorSubject()
        subject.subscribe_teacher(ValidatorTeacher())
        assert subject.has_teacher() is True


class TestSubjectMinimumInProgressStudents:
    _inprogress = ValidatorStudent()
    _inprogress.force_state(StudentInProgress())

    def test_subject_has_no_minimum_students_when_created(self):
        subject = ValidatorSubject()
        assert subject.has_minimum_inprogress_students() is False

    def test_subject_has_no_minimum_students_when_minimum_not_added(self):
        subject = ValidatorSubject()
        for _ in range(2):
            subject.accept_student(self._inprogress)
        assert subject.has_minimum_inprogress_students() is False

    def test_subject_has_minimum_students_when_minimum_added(self):
        subject = ValidatorSubject()
        for _ in range(3):
            subject.accept_student(self._inprogress)
        assert subject.has_minimum_inprogress_students() is True


class TestSubjectMaximumInProgressStudents:
    _inprogress = ValidatorStudent()
    _inprogress.force_state(StudentInProgress())

    def test_subject_has_no_maximum_students_when_created(self):
        subject = ValidatorSubject()
        assert subject.has_maximum_students() is False

    def test_subject_has_no_maximimum_students_when_maximum_not_added(self):
        subject = ValidatorSubject()
        for _ in range(2):
            subject.accept_student(self._inprogress)
        assert subject.has_maximum_students() is False

    def test_subject_has_maximum_students_when_maximum_added(self, caplog):
        caplog.set_level(logging.ERROR)
        subject = ValidatorSubject()
        for _ in range(30):
            subject.accept_student(self._inprogress)
        assert subject.has_maximum_students() is True


class TestSubjectAcceptedStudents:
    def test_subject_has_no_students_when_created(self):
        subject = ValidatorSubject()
        assert len(subject.list_all_students()) == 0

    def test_subject_has_one_student_when_one_added(self):
        subject = ValidatorSubject()
        subject.accept_student(ValidatorStudent())
        assert len(subject.list_all_students()) == 1

    def test_subject_has_one_inprogress_student_when_one_added(self):
        subject = ValidatorSubject()
        student = ValidatorStudent()
        student2 = ValidatorStudent()
        student2.force_state(StudentInProgress())
        subject.accept_student(student2)
        subject.accept_student(student)
        assert len(subject.list_all_inprogress_students()) == 1
        assert len(subject.list_all_students()) == 2
