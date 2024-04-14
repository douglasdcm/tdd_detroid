import sqlite3
import logging
from src import utils


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
        subjects = None
        course = None

        def __init__(self, con, cur):
            self.cur = cur
            self.con = con
            # TODO move to installation file
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name, state, cpf, identifier, gpa, subjects, course)"
            )

        def add(self):
            try:
                cmd = f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{self.name}', 
                        '{self.state}', 
                        '{self.cpf}', 
                        '{self.identifier}', 
                        '{self.gpa}', 
                        '{self.subjects}', 
                        '{self.course}')
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
                    gpa = '{self.gpa}',
                    subjects = '{self.subjects}'
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
                        '{course_identifier}')
                """
            )
            self.con.commit()

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
                self.gpq = result[4]
                self.subjects = result[5].split(",")
                self.course = result[6]
            except Exception as e:
                logging.error(str(e))
                raise

    class DbEnrollment:
        TABLE = "enrollment"

        def __init__(self, con, cur):
            self.cur = cur
            self.con = con
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (student_identifier)"
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
        subjects = None

        def __init__(self, con, cur):
            self.con = con
            self.cur = cur
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name, state, identifier, enrolled_students, max_enrollment, subjects)"
            )

        # Just for admin. Necessary because there is not a user story to create courses
        # TODO create a public funtion
        def populate(self, name):
            identifier = utils.generate_course_identifier(name)
            self.cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{name}', 
                        'active', 
                        '{identifier}', 
                        '', 
                        '10', 
                        'any1,any2,any3')
                """
            )
            self.con.commit()

        def save(self):
            try:
                self.cur.execute(
                    f"""
                        INSERT INTO {self.TABLE} VALUES
                            ('{self.name}', 
                            '{self.state}', 
                            '{self.identifier}', 
                            '{self.enrolled_students}', 
                            '{self.max_enrollment}', 
                            '{self.subjects}')
                    """
                )
                self.con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def load_from_database(self, name):
            result = self.cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE name = '{name}'"
            ).fetchone()
            self.name = result[0]
            self.state = result[1]
            self.identifier = result[2]
            self.enrolled_students = result[3].split(",")
            self.max_enrollment = result[4]
            self.subjects = result[5].split(",")

    class DbSubject:
        TABLE = "subject"
        name = None
        state = None
        enrolled_students = None
        max_enrollment = None
        identifier = None
        course = None

        def __init__(self, con, cur):
            self.cur = cur
            self.con = con
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name, state, identifier, enrolled_students, max_enrollment, course)"
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
                    raise NotFoundError()

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
        TABLE = "grade_calculator"
        student_identifier = None
        subject_identifier = None
        grade = None

        def __init__(self, con, cur):
            self.con = con
            self.cur = cur
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (student_identifier, subject_identifier, grade)"
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

                class GradeCalculatorRow:
                    student_identifier = None
                    subject_identifier = None
                    grade = None

                grade_calculators = []
                for row in result:
                    grade_calculator_row = GradeCalculatorRow()
                    grade_calculator_row.student_identifier = row[0]
                    grade_calculator_row.subject_identifier = row[1]
                    grade_calculator_row.grade = row[2]
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
                    raise NotFoundError()

                self.student_identifier = result[0]
                self.subject_identifier = result[1]
                self.grade = result[2]
            except Exception as e:
                logging.error(str(e))
                raise

        def add(self):
            try:
                cmd = f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{self.student_identifier}', 
                        '{self.subject_identifier}', 
                        {self.grade})
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
                    SET student_identifier = '{self.student_identifier}',
                        subject_identifier = '{self.subject_identifier}',
                        grade = {self.grade}
                    WHERE student_identifier = '{self.student_identifier}';
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

            x = self.cur.execute(f"select * from {self.TABLE}").fetchall()

        def save(self):
            try:
                cmd = f"""
                    UPDATE {self.TABLE}
                    SET state = '{self.state}'
                    WHERE identifier = '{self.identifier}';
                    """
                self.cur.execute(cmd)

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
