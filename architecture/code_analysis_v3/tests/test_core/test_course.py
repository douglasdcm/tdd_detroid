from pytest import fixture, raises
from architecture.code_analysis_v3.core.course import (
    AbstractCourse,
    CourseInProgress,
    CourseNotStarted,
)
from architecture.code_analysis_v3.core.exceptions import InvalidStudent, InvalidSubject
from architecture.code_analysis_v3.core.student import Student
from architecture.code_analysis_v3.core.subject import Subject
from architecture.code_analysis_v3.tests.test_core.test_constants import ANY_NAME
from architecture.code_analysis_v3.tests.test_core.validator_classes import (
    ValidatorCourse,
    ValidatorSubject,
)


@fixture
def course():
    yield ValidatorCourse(ANY_NAME)


class TestCourseStateTransition:
    def test_course_notstarted_when_created(self, course: AbstractCourse):
        assert isinstance(course.state, CourseNotStarted)

    def test_course_inprogress_when_has_minimum_student_and_minimum_subjects(
        self, course: ValidatorCourse
    ):
        course.force_has_minimum_students()
        course.force_has_minimum_subjects()
        assert isinstance(course.state, CourseInProgress)

    def test_course_state_does_not_changed_when_inprogress(self, course: ValidatorCourse):
        course.force_state(CourseInProgress())
        assert isinstance(course.state, CourseInProgress)


class TestCourseAcceptStudent:
    def test_course_has_no_student_when_created(self, course: AbstractCourse):
        assert len(course.list_all_students()) == 0

    def test_course_has_one_student_when_student_accepted(self, course: AbstractCourse):
        course.accept_student(Student(ANY_NAME))
        assert len(course.list_all_students()) == 1

    def test_course_does_not_accept_students_when_full_of_students(self, course: ValidatorCourse):
        course.force_is_full_of_students()
        with raises(InvalidStudent):
            course.accept_student(Student(ANY_NAME))

    def test_course_does_not_accept_student_when_student_already_in_course(
        self, course: ValidatorCourse
    ):
        student = Student(ANY_NAME)
        course.force_students(student)
        course.accept_student(student)
        assert len(course.list_all_students()) == 1

    def test_course_does_not_accept_student_when_student_in_other_course(
        self, course: ValidatorCourse
    ):
        student = Student(ANY_NAME)
        student.course = ValidatorCourse(ANY_NAME)
        with raises(InvalidStudent):
            course.accept_student(student)


class TestCourseAcceptSubject:
    def test_course_has_no_subjects_when_created(self, course: AbstractCourse):
        assert len(course.list_all_subjects()) == 0

    def test_course_has_one_subject_when_subject_accepted(self, course: AbstractCourse):
        course.accept_subject(Subject(ANY_NAME))
        assert len(course.list_all_subjects()) == 1

    def test_course_does_not_accept_subject_when_full_of_subjects(self, course: ValidatorCourse):
        course.force_is_full_of_subjects()
        with raises(InvalidSubject):
            course.accept_subject(Subject(ANY_NAME))

    def test_course_does_not_accept_subject_when_subject_already_in_course(
        self, course: ValidatorCourse
    ):
        subject = ValidatorSubject(ANY_NAME)
        course.force_subject(subject)
        with raises(InvalidSubject):
            course.accept_subject(subject)

    def test_course_does_not_accept_subject_when_subject_in_other_course(
        self, course: ValidatorCourse
    ):
        subject = ValidatorSubject(ANY_NAME)
        course.force_subject(subject)
        with raises(InvalidSubject):
            course.accept_subject(subject)
