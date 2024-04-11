import sqlite3
import logging

# TODO test concurrency
DATABASE_NAME = ":memory:"
con = sqlite3.connect(DATABASE_NAME)
cur = con.cursor()


class Database:
    class DbStudent:
        TABLE = "student"
        name = None
        state = None
        cpf = None
        identifier = None
        gpa = None
        subjects = None
        course = None

        def save(self):
            cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{self.name}', 
                        '{self.state}', 
                        '{self.cpf}', 
                        '{self.identifier}', 
                         {self.gpa}, 
                        '{self.subjects}', 
                        '{self.course}')
                """
            )
            con.commit()

        def __init__(self):
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name, state, cpf, identifier, gpa, subjects, course)"
            )

        def load(self, identifier):
            result = cur.execute(
                f"SELECT * FROM {self.TABLE} WHERE identifier = '{identifier}'"
            ).fetchone()
            self.name = result[0]
            self.state = result[1]
            self.cpf = result[2]
            self.identifier = result[3]
            self.gpq = result[4]
            self.subjects = result[5].split(",")
            self.course = result[6]

    class DbEnrollment:
        TABLE = "enrollment"

        def __init__(self):
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.TABLE} (student_identifier)")

        # Just for admin. The university has a predefined list of approved students to each course.
        # TODO create a public funtion
        def populate(self, name, cpf, course_identifier):
            import uuid

            student_identifier = uuid.uuid5(
                uuid.NAMESPACE_URL, str(f"{name}{cpf}{course_identifier}")
            ).hex
            cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES ('{student_identifier}')
                """
            )
            con.commit()

        def select(self, student_identifier):
            return (
                cur.execute(
                    f"SELECT * FROM {self.TABLE} WHERE student_identifier = '{student_identifier}'"
                ).fetchone()
                is not None
            )

    class DbCourse:
        TABLE = "course"
        name = None
        state = None
        identifier = None
        enrolled_students = None
        max_enrollment = None
        subjects = None

        def __init__(self):
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name, state, identifier, enrolled_students, max_enrollment, subjects)"
            )

        # Just for admin. Necessary because there is not a user story to create courses
        # TODO create a public funtion
        def populate(self, name):
            import uuid

            identifier = uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}")).hex
            cur.execute(
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
            con.commit()

        def save(self):
            try:
                cur.execute(
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
                con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

        def load_from_database(self, name):
            result = cur.execute(
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

        def __init__(self):
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {self.TABLE} (name, state, identifier, enrolled_students, max_enrollment, course)"
            )

        # Just for admin. The university has a predefined list of approved students to each course.
        # TODO create a public funtion
        def populate(self, course, name, max_enrollment=10):
            import uuid

            identifier = uuid.uuid5(uuid.NAMESPACE_URL, str(f"{name}{course}")).hex
            cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{name}', 
                        'active', 
                        '{identifier}', 
                        '', 
                        {max_enrollment}, 
                        '{course}')
                """
            )
            con.commit()

        def load(self, subject_identifier):
            try:
                result = cur.execute(
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
                        max_enrollment = '{self.max_enrollment}'
                    WHERE identifier = '{self.identifier}';
                    """
                cur.execute(cmd)

                con.commit()
            except Exception as e:
                logging.error(str(e))
                raise

    student = DbStudent()
    enrollment = DbEnrollment()
    course = DbCourse()
    subject = DbSubject()


class NotFoundError(Exception):
    pass
