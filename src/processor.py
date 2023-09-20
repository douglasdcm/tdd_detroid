from multiprocessing import Lock, Process


def grade_students_in_parallel(students, grades, queue=None):
    lock = Lock()

    def task(student, grade):
        with lock:
            student.grade_course(grade)
            if queue:
                queue.put(student)

    processes = []
    i = 0
    for student in students:
        processes.append(Process(target=task, args=(student, grades[i])))
        i += 1

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return True
