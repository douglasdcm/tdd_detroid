import sqlite3
import logging
from src import utils


def convert_csv_to_list(the_csv):
    if len(the_csv) == 0 or the_csv is None:
        return []
    return the_csv.split(",")


def convert_list_to_csv(the_list):
    return ",".join(set(the_list))


# TODO test concurrency
class Database:

    def __init__(self, database="university.db"):
        con = sqlite3.connect(database)
        cur = con.cursor()
        self.student = self.DbStudent(con, cur)
        self.enrollment = self.DbEnrollment(con, cur)
        self.course = self.DbCourse(con, cur)
        self.subject = self.DbSubject(con, cur)
        self.grade_calculator = self.DbGradeCalculator(con, cur)
        self.semester = self.DbSemester(con, cur)

    class DbStudent:
        TABLE = "student"
        name = None
        state = None
        cpf = None
        identifier = None
        gpa = None
        subjects = []
        course = None
        semester_counter = None

        def __init__(self, con, cur):
            self.cur = cur
            self.con = con
            # TODO move to installation file
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name,"
                " state,"
                " cpf,"
                " identifier,"
                " gpa,"
                " subjects,"
                " course,"
                " semester_counter)"
            )

        def add(self):
            try:
                cmd = f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{self.name}', 
                        '{self.state}', 
                        '{self.cpf}', 
                        '{self.identifier}', 
                         {self.gpa}, 
                        '{convert_list_to_csv(self.subjects)}', 
                        '{self.course}',
                        {self.semester_counter})
                """
                self.cur.execute(cmd)

                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def save(self):
            cmd = f"""
                UPDATE {self.TABLE}
                SET state = '{self.state}',
                    gpa = {self.gpa},
                    semester_counter = {self.semester_counter},
                    subjects = '{convert_list_to_csv(self.subjects)}'
                WHERE identifier = '{self.identifier}';
                """
            self.cur.execute(cmd)

            self.con.commit()

        # Just for admin.
        # TODO create a public funtion
        def populate(
            self, name, cpf, course_identifier, state="enrolled", gpa=0, subject=""
        ):
            student_identifier = utils.generate_student_identifier(
                name, cpf, course_identifier
            )
            self.cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES (
                        '{name}',
                        '{state}',
                        '{cpf}',
                        '{student_identifier}',
                        '{gpa}',
                        '{subject}',
                        '{course_identifier}',
                        0)
                """
            )
            self.con.commit()

        def search_all(self):
            class StudentRow:
                name = None
                state = None
                cpf = None
                identifier = None
                gpa = None
                subjects = None
                course = None
                semester_counter = None

            try:
                cmd = f"SELECT * FROM {self.TABLE}"
                result = self.cur.execute(cmd).fetchall()
                if not result:
                    return []
                student_rows = []
                for row in result:
                    student_row = StudentRow()
                    student_row.name = row[0]
                    student_row.state = row[1]
                    student_row.cpf = row[2]
                    student_row.identifier = row[3]
                    student_row.gpa = row[4]
                    student_row.subjects = convert_csv_to_list(row[5])
                    student_row.course = row[6]
                    student_row.semester_counter = row[7]
                    student_rows.append(student_row)
                return student_rows
            except Exception as e:
                logging.error(str(e))
                raise

        def load(self, identifier):
            try:
                cmd = f"SELECT * FROM {self.TABLE} WHERE identifier = '{identifier}'"
                result = self.cur.execute(cmd).fetchone()
                if not result:
                    raise NotFoundError(
                        f"Student '{self.identifier}' not found in table '{self.TABLE}'."
                    )
                self.name = result[0]
                self.state = result[1]
                self.cpf = result[2]
                self.identifier = result[3]
                self.gpa = result[4]
                self.subjects = convert_csv_to_list(result[5])
                self.course = result[6]
                self.semester_counter = result[7]
            except Exception as e:
                logging.error(str(e))
                raise

    class DbEnrollment:
        TABLE = "enrollment"

        def __init__(self, con, cur):
            self.cur = cur
            self.con = con
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (student_identifier TEXT NOT NULL UNIQUE)"
            )

        # Just for admin. The university has a predefined list of approved students to each course.
        # TODO create a public funtion
        def populate(self, name, cpf, course_name):
            student_identifier = utils.generate_student_identifier(
                name, cpf, course_name
            )
            self.cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES ('{student_identifier}')
                """
            )
            self.con.commit()

        def select(self, student_identifier):
            cmd = f"SELECT * FROM {self.TABLE} WHERE student_identifier = '{student_identifier}'"
            return self.cur.execute(cmd).fetchone() is not None

    class DbCourse:
        TABLE = "course"
        name = None
        state = None
        identifier = None
        enrolled_students = None
        max_enrollment = None
        subjects = []

        def __init__(self, con, cur):
            self.con = con
            self.cur = cur
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE}"
                " (name TEXT NOT NULL UNIQUE,"
                " state TEXT NOT NULL,"
                " identifier TEXT NOT NULL UNIQUE,"
                " enrolled_students TEXT,"
                " max_enrollment INTEGER NOT NULL,"
                " subjects TEXT)"
            )

        # Just for admin. Necessary because there is not a user story to create courses
        # TODO create a public funtion
        def populate(self, name, state="active", subjects="any1,any2,any3"):
            identifier = utils.generate_course_identifier(name)
            subjects = subjects.split(",")
            list_of_subjects = []
            for subject in subjects:
                subject_identifier = utils.generate_subject_identifier(name, subject)
                list_of_subjects.append(subject_identifier)
            self.cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{name}', 
                        '{state}', 
                        '{identifier}', 
                        '', 
                        10, 
                        '{",".join(list_of_subjects)}')
                """
            )
            self.con.commit()

        def save(self):
            try:
                cmd = f"""
                    UPDATE {self.TABLE}
                    SET enrolled_students = '{convert_list_to_csv(self.enrolled_students)}',
                    state = '{self.state}',
                    max_enrollment = '{self.max_enrollment}',
                    subjects = '{convert_list_to_csv(self.subjects)}'
                    WHERE identifier = '{self.identifier}';
                    """
                self.cur.execute(cmd)
                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def add(self):
            try:
                self.cur.execute(
                    f"""
                        INSERT INTO {self.TABLE} VALUES
                            ('{self.name}', 
                            '{self.state}', 
                            '{self.identifier}', 
                            '{convert_list_to_csv(self.enrolled_students)}', 
                            {self.max_enrollment}, 
                            '{convert_list_to_csv(self.subjects)}')
                    """
                )
                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def search_all(self):
            result = self.cur.execute(f"SELECT * FROM {self.TABLE}").fetchall()

            class CourseRow:
                name = None
                state = None
                identifier = None
                enrolled_students = None
                max_enrollment = None
                subjects = None

            courses = []
            for row in result:
                course_row = CourseRow()
                course_row.name = row[0]
                course_row.state = row[1]
                course_row.identifier = row[2]
                course_row.enrolled_students = convert_csv_to_list(the_csv=row[3])
                course_row.max_enrollment = row[4]
                course_row.subjects = convert_csv_to_list(row[5])
                courses.append(course_row)
            return courses

        def load_from_database(self, name):
            try:
                result = self.cur.execute(
                    f"SELECT * FROM {self.TABLE} WHERE name = '{name}'"
                ).fetchone()
                if not result:
                    raise NotFoundError(
                        f"Course '{name}' not found in table {self.TABLE}."
                    )
                self.name = result[0]
                self.state = result[1]
                self.identifier = result[2]
                self.enrolled_students = convert_csv_to_list(the_csv=result[3])
                self.max_enrollment = result[4]
                self.subjects = convert_csv_to_list(result[5])
            except Exception as e:
                logging.error(str(e))
                raise

    class DbSubject:
        TABLE = "subject"
        name = None
        state = None
        enrolled_students = None
        max_enrollment = None
        identifier = None
        course = None
        MAX_ENROLLMENT = 30

        def __init__(self, con, cur):
            self.cur = cur
            self.con = con
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE}"
                " (name, state, identifier, enrolled_students,"
                f" max_enrollment CHECK (max_enrollment <= {self.MAX_ENROLLMENT}) , course)"
            )

        # Just for admin. The university has a predefined list of approved students to each course.
        # TODO create a public funtion
        def populate(self, course, name, max_enrollment=10, state="active"):
            identifier = utils.generate_subject_identifier(course, name)
            self.cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{name}', 
                        '{state}', 
                        '{identifier}', 
                        '', 
                        {max_enrollment}, 
                        '{course}')
                """
            )
            self.con.commit()

        def load(self, subject_identifier):
            try:
                result = self.cur.execute(
                    f"SELECT * FROM {self.TABLE} WHERE identifier = '{subject_identifier}'"
                ).fetchone()
                if not result:
                    raise NotFoundError(
                        f"Subject '{subject_identifier}' not found in table '{self.TABLE}'"
                    )

                self.name = result[0]
                self.state = result[1]
                self.identifier = result[2]
                self.enrolled_students = result[3].split(",")
                self.max_enrollment = result[4]
                self.course = result[5]
            except Exception as e:
                logging.error(str(e))
                raise

        def save(self):
            try:
                cmd = f"""
                    UPDATE {self.TABLE}
                    SET state = '{self.state}',
                        enrolled_students = '{self.enrolled_students}',
                        max_enrollment = {self.max_enrollment}
                    WHERE identifier = '{self.identifier}';
                    """
                self.cur.execute(cmd)

                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

    class DbGradeCalculator:
        class GradeCalculatorRow:
            student_identifier = None
            subject_identifier = None
            grade = None
            subject_situation = None

        TABLE = "grade_calculator"
        student_identifier = None
        subject_identifier = None
        grade = None
        subject_situation = None

        def __init__(self, con, cur):
            self.con = con
            self.cur = cur
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (student_identifier,"
                " subject_identifier,"
                " grade INTEGER,"
                " subject_situation)"
            )

        def load_all_by_student_identifier(self, student_identifier):
            try:
                cmd = f"""SELECT * FROM {self.TABLE}
                        WHERE student_identifier = '{student_identifier}'
                    """
                result = self.cur.execute(cmd).fetchall()
                if not result:
                    raise NotFoundError(
                        f"Student '{student_identifier}' not found in table '{self.TABLE}'"
                    )

                grade_calculators = []
                for row in result:
                    grade_calculator_row = self.GradeCalculatorRow()
                    grade_calculator_row.student_identifier = row[0]
                    grade_calculator_row.subject_identifier = row[1]
                    grade_calculator_row.grade = row[2]
                    grade_calculator_row.subject_situation = row[3]
                    grade_calculators.append(grade_calculator_row)
                return grade_calculators
            except Exception as e:
                logging.error(str(e))
                raise

        def search(self, student_identifier, subject_identifier):
            try:
                result = self.cur.execute(
                    f"""SELECT * FROM {self.TABLE}
                        WHERE subject_identifier = '{subject_identifier}'
                        AND student_identifier = '{student_identifier}'
                    """
                ).fetchone()
                if not result:
                    return

                grade_calculator_row = self.GradeCalculatorRow()
                grade_calculator_row.student_identifier = result[0]
                grade_calculator_row.subject_identifier = result[1]
                grade_calculator_row.grade = result[2]
                grade_calculator_row.subject_situation = result[3]

                return grade_calculator_row
            except Exception as e:
                logging.error(str(e))
                raise

        def search_all(self):
            try:
                result = self.cur.execute(f"""SELECT * FROM {self.TABLE}""").fetchall()
                if not result:
                    return

                grade_calculators = []
                for row in result:
                    grade_calculator_row = self.GradeCalculatorRow()
                    grade_calculator_row.student_identifier = row[0]
                    grade_calculator_row.subject_identifier = row[1]
                    grade_calculator_row.grade = row[2]
                    grade_calculator_row.subject_situation = row[3]
                    grade_calculators.append(grade_calculator_row)

                return grade_calculators
            except Exception as e:
                logging.error(str(e))
                raise

        def load(self, student_identifier, subject_identifier):
            try:
                result = self.cur.execute(
                    f"""SELECT * FROM {self.TABLE}
                        WHERE subject_identifier = '{subject_identifier}'
                        AND student_identifier = '{student_identifier}'
                    """
                ).fetchone()
                if not result:
                    raise NotFoundError(
                        f"Student '{student_identifier}' and subject '{subject_identifier}'"
                        f" not found in table '{self.TABLE}'."
                    )

                self.student_identifier = result[0]
                self.subject_identifier = result[1]
                self.grade = result[2]
                self.subject_situation = result[3]
            except Exception as e:
                logging.error(str(e))
                raise

        def add(self):
            try:
                cmd = f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{self.student_identifier}', 
                        '{self.subject_identifier}', 
                        {self.grade},
                        '{self.subject_situation}')
                """
                self.cur.execute(cmd)

                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def save(self):
            try:
                cmd = f"""
                    UPDATE {self.TABLE}
                    SET grade = {self.grade},
                        subject_situation = '{self.subject_situation}'
                    WHERE student_identifier = '{self.student_identifier}'
                    AND subject_identifier = '{self.subject_identifier}';
                    """
                self.cur.execute(cmd)

                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def remove(self, student_identifier, subject_identifier):
            try:
                cmd = f"""
                    DELETE FROM {self.TABLE}
                    WHERE student_identifier = '{student_identifier}'
                    AND subject_identifier = '{subject_identifier}';
                    """
                self.cur.execute(cmd)

                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

    class DbSemester:
        TABLE = "semester"
        identifier = None
        state = None

        def __init__(self, con, cur):
            self.con = con
            self.cur = cur
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.TABLE} (identifier, state)")

        # Just for admin.
        # TODO create a public funtion
        def populate(self, identifier, state):
            self.cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{identifier}', 
                        '{state}')
                """
            )
            self.con.commit()
            self.cur.execute(f"select * from {self.TABLE}").fetchall()

        def save(self):
            try:
                cmd = f"""
                    UPDATE {self.TABLE}
                    SET state = '{self.state}'
                    WHERE identifier = '{self.identifier}';
                    """
                result = self.cur.execute(cmd)

                if not result:
                    raise NotFoundError(
                        f"Semester '{self.identifier}' not found in table '{self.TABLE}'"
                    )

                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def load_open(self):
            try:
                result = self.cur.execute(
                    f"""SELECT * FROM {self.TABLE}
                        WHERE state = 'open'
                    """
                ).fetchone()

                if not result:
                    raise NotFoundError("No open semester found")

                self.identifier = result[0]
                self.state = result[1]
            except Exception as e:
                logging.error(str(e))
                raise

        def load_by_identifier(self):
            try:
                result = self.cur.execute(
                    f"""SELECT * FROM {self.TABLE}
                        WHERE identifier = '{self.identifier}'
                    """
                ).fetchone()
                if not result:
                    raise NotFoundError(f"Semester '{self.identifier}' not found")

                self.identifier = result[0]
                self.state = result[1]
            except Exception as e:
                logging.error(str(e))
                raise


class NotFoundError(Exception):
    pass
