from pytest import fixture, raises
from architecture.code_analysis_v3.core.course import (
    CourseInProgress,
    CourseNotStarted,
)
from architecture.code_analysis_v3.core.exceptions import InvalidStudent, InvalidSubject
from architecture.code_analysis_v3.core.student import StudentInProgress
from architecture.code_analysis_v3.core.subject import SubjectInProgress
from architecture.code_analysis_v3.tests.test_core.validator_classes import (
    ValidatorCourse,
    ValidatorStudent,
    ValidatorSubject,
)


@fixture
def course():
    yield ValidatorCourse()


class TestCourseStateTransition:
    def test_course_notstarted_when_created(self, course: ValidatorCourse):
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
    def test_course_has_no_student_when_created(self, course: ValidatorCourse):
        assert len(course.list_all_students()) == 0

    def test_course_has_one_student_when_student_accepted(self, course: ValidatorCourse):
        course.accept_student(ValidatorStudent())
        assert len(course.list_all_students()) == 1

    def test_course_does_not_accept_students_when_full_of_students(self, course: ValidatorCourse):
        course.force_is_full_of_students()
        with raises(InvalidStudent):
            course.accept_student(ValidatorStudent())

    def test_course_does_not_accept_student_when_student_already_in_course(
        self, course: ValidatorCourse
    ):
        student = ValidatorStudent()
        course.force_students(student)
        with raises(InvalidStudent):
            course.accept_student(student)

    def test_course_does_not_accept_student_when_student_in_other_course(
        self, course: ValidatorCourse
    ):
        student = ValidatorStudent()
        student.course = ValidatorCourse()
        with raises(InvalidStudent):
            course.accept_student(student)


class TestCourseAcceptSubject:
    def test_course_has_no_subjects_when_created(self, course: ValidatorCourse):
        assert len(course.list_all_subjects()) == 0

    def test_course_has_one_subject_when_subject_accepted(self, course: ValidatorCourse):
        course.accept_subject(ValidatorSubject())
        assert len(course.list_all_subjects()) == 1

    def test_course_does_not_accept_subject_when_full_of_subjects(self, course: ValidatorCourse):
        course.force_is_full_of_subjects()
        with raises(InvalidSubject):
            course.accept_subject(ValidatorSubject())

    def test_course_does_not_accept_subject_when_subject_already_in_course(
        self, course: ValidatorCourse
    ):
        subject = ValidatorSubject()
        course.force_subject(subject)
        with raises(InvalidSubject):
            course.accept_subject(subject)

    def test_course_does_not_accept_subject_when_subject_in_other_course(
        self, course: ValidatorCourse
    ):
        subject = ValidatorSubject()
        course.force_subject(subject)
        with raises(InvalidSubject):
            course.accept_subject(subject)


class TestIsFullOfSubjects:
    def test_course_is_full_of_subjects_when_maximum_subjects_added(self, course: ValidatorCourse):
        for _ in range(30):
            course.accept_subject(ValidatorSubject())
        with raises(InvalidSubject):
            course.accept_subject(ValidatorSubject())


class TestIsFullOfStudents:
    def test_course_is_full_of_students_when_maximum_students_added(self, course: ValidatorCourse):
        for _ in range(900):
            course.accept_student(ValidatorStudent())
        with raises(InvalidStudent):
            course.accept_student(ValidatorStudent())

    def test_course_is_not_full_of_students_when_maximum_students_not_added(
        self, course: ValidatorCourse
    ):
        for _ in range(899):
            course.accept_student(ValidatorStudent())
        assert course.is_full_of_student() is False


class TestHasMinimumStudents:
    def test_course_has_minimum_students_when_minimum_students_added(self, course: ValidatorCourse):
        for _ in range(9):
            student = ValidatorStudent()
            student.force_state(StudentInProgress())
            course.accept_student(student)
        assert course.has_minimum_inprogress_students() is True

    def test_course_has_not_minimum_students_when_minimum_students_not_added(
        self, course: ValidatorCourse
    ):
        for _ in range(2):
            course.accept_student(ValidatorStudent())
        assert course.has_minimum_inprogress_students() is False

    def test_course_has_not_minimum_students_when_minimum_students_added_but_not_in_progress(
        self, course: ValidatorCourse
    ):
        for _ in range(9):
            course.accept_student(ValidatorStudent())
        assert course.has_minimum_inprogress_students() is False


class TestHasMinimumSubject:
    def test_course_has_minimum_subject_when_minimum_added(self, course: ValidatorCourse):
        for _ in range(9):
            subject = ValidatorSubject()
            subject.force_state(SubjectInProgress())
            course.accept_subject(subject)
        assert course.has_minimum_inprogress_subjects() is True

    def test_course_has_not_minimum_subject_when_minimum_students_not_added(
        self, course: ValidatorCourse
    ):
        for _ in range(2):
            course.accept_subject(ValidatorSubject())
        assert course.has_minimum_inprogress_subjects() is False

    def test_course_has_not_minimum_subject_when_minimum_students_added_but_not_in_progress(
        self, course: ValidatorCourse
    ):
        for _ in range(3):
            course.accept_subject(ValidatorSubject())
        assert course.has_minimum_inprogress_subjects() is False
