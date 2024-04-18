import pytest
from src.services.student_handler import StudentHandler
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler
from src.services.semester_monitor import SemesterMonitor
from src.constants import MAX_SEMESTERS_TO_FINISH_COURSE


def __get_subjects():
    subjects = [
        "mgmt",
        "people1",
        "people2",
        "people3",
        "strategy1",
        "strategy2",
        "strategy3",
        "business1",
        "business2",
        "business3",
    ]

    return subjects


def __update_grade_of_3_subjects_only(grade, subjects, student_handler):
    for i in range(3):
        student_handler.take_subject(subjects[i])
        student_handler.update_grade_to_subject(grade, subjects[i])


def __close_maximum_semesters(database):
    for i in range(MAX_SEMESTERS_TO_FINISH_COURSE + 1):
        semester_monitor = SemesterMonitor(database, f"1234-{i+1}")
        semester_monitor.close()


def __update_grade_of_all_subjects(grade, subjects, student_handler):
    for subject in subjects:
        student_handler.take_subject(subject)
        student_handler.update_grade_to_subject(grade, subject)


def __enroll_student_to_course(course, database):
    student_handler = StudentHandler(database)
    student_handler.name = "douglas"
    student_handler.cpf = "098.765.432.12"
    student_handler.enroll_to_course(course)
    return student_handler


def __add_all_subjects_to_course(course, subjects, database):
    course_handler = CourseHandler(database)
    course_handler.name = course
    for subject in subjects:
        course_handler.add_subject(subject)
        subject_handler = SubjectHandler(database)
        subject_handler.name = subject
        subject_handler.course = course
        subject_handler.max_enrollment = 5
        subject_handler.activate()
    course_handler.activate()


def test_student_locked_by_minimun_subjects_per_semester():
    pass


def test_student_can_enroll_to_course_after_fail_it_losing_all_history():
    pass


def test_student_cannot_do_anythin_after_pass_or_fail_course():
    pass


def test_coordinator_cancel_course_before_studend_conclude_it_not_affecting_grades():
    pass


def test_coordinator_cancel_course_before_studend_conclude_it_not_affecting_student_situation():
    pass


def test_student_locks_course_and_forget_and_fail_by_maximum_semesters():
    pass


def test_student_failed_by_maximum_semesters(set_in_memory_database):
    course = "adm"
    grade = 9
    situation = "failed"
    database = set_in_memory_database

    subjects = __get_subjects()
    __add_all_subjects_to_course(course, subjects, database)
    student_handler = __enroll_student_to_course(course, database)
    __update_grade_of_3_subjects_only(grade, subjects, student_handler)
    __close_maximum_semesters(database)

    assert student_handler.semester_counter == MAX_SEMESTERS_TO_FINISH_COURSE + 1
    assert student_handler.gpa == grade
    assert student_handler.state == situation


@pytest.mark.parametrize(
    "grade,situation",
    [
        (7, "approved"),
        (5, "failed"),
    ],
)
def test_student_finishes_course(set_in_memory_database, grade, situation):
    course = "adm"
    database = set_in_memory_database

    subjects = __get_subjects()
    __add_all_subjects_to_course(course, subjects, database)
    student_handler = __enroll_student_to_course(course, database)
    __update_grade_of_all_subjects(grade, subjects, student_handler)
    __close_maximum_semesters(database)

    assert student_handler.semester_counter == MAX_SEMESTERS_TO_FINISH_COURSE + 1
    assert student_handler.gpa == grade
    assert student_handler.state == situation
