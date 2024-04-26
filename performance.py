import multiprocessing
from src.services.student_handler import StudentHandler
from src.services.course_handler import CourseHandler
from src.services.subject_handler import SubjectHandler
from src.services.semester_monitor import SemesterMonitor
from src.constants import MAX_SEMESTERS_TO_FINISH_COURSE, MAX_ENROLLMENT_TO_SUBJECT
from src.database import Database

DATABASE = Database()
COURSE = "adm"


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


def __close_maximum_semesters(database):
    semester_monitor = SemesterMonitor(database, "1234-1")
    semester_monitor.close()


def __update_grade_of_all_subjects(grade, subjects, student_handler):
    for subject in subjects:
        student_handler.take_subject(subject)
        student_handler.update_grade_to_subject(grade, subject)


def __enroll_student_to_course(student_name, course, database):
    student_handler = StudentHandler(database)
    student_handler.name = student_name
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
        subject_handler.max_enrollment = MAX_ENROLLMENT_TO_SUBJECT
        subject_handler.activate()
    course_handler.activate()
    return course_handler


def student_finishes_course(student_name, lock):
    with lock:
        grade = 7
        student_handler = __enroll_student_to_course(student_name, COURSE, DATABASE)
        __update_grade_of_all_subjects(grade, subjects, student_handler)


if __name__ == "__main__":
    subjects = __get_subjects()
    __add_all_subjects_to_course(COURSE, subjects, DATABASE)

    lock = multiprocessing.Lock()

    processes = []
    for i in range(MAX_ENROLLMENT_TO_SUBJECT - 1):
        processes.append(
            multiprocessing.Process(
                target=student_finishes_course,
                args=(
                    f"student{i}",
                    lock,
                ),
            )
        )

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    __close_maximum_semesters(DATABASE)
