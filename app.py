from src.student import Student
from src.context import students
from src.processor import grade_students_in_parallel
from multiprocessing import Queue

MENU = """
----------
Command:
1 create new student
2 grade student
3 grade student in parallel
4 list all students
----------
"""


def main():
    while True:
        command = input(MENU)
        if command == "1":
            new_student = Student()
            students.append(new_student)
            print(f"{len(students)} new student created")

        if command == "2":
            id = int(input("student id (index): "))
            grade = int(input("student grade (int): "))
            try:
                students[id].grade_course(grade)
                print(f"Student final grade: {students[id].get_grade()}")
            except Exception as error:
                print("No student found")
                print(str(error))

        if command == "3":
            queue = Queue()
            student_ids = input("List of student ids (int): ").split(",")
            grades = input("List of grades (int): ").split(",")

            informed_students = []
            for id in student_ids:
                try:
                    informed_students.append(students[int(id)])
                except Exception as error:
                    print(f"Student '{id}' not found")
                    print(str(error))

            informed_grades = []
            for grade in grades:
                informed_grades.append(int(grade))

            grade_students_in_parallel(informed_students, informed_grades, queue)

            # updated_student = []
            # while queue.qsize():
            #     updated_student.append(queue.get())

            for id in student_ids:
                students[int(id)] = queue.get()
                try:
                    print(
                        f"Student '{students[int(id)]}' grade is '{students[int(id)].get_grade()}'"
                    )
                except Exception as error:
                    print(f"ERROR: {str(error)}")

        if command == "4":
            print(f"list of students: {len(students)}")


if __name__ == "__main__":
    main()
