import sqlite3

# TODO test concurrency
DATABASE_NAME = "university.db"
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
                        '[]', 
                        '10', 
                        '[]')
                """
            )
            con.commit()

        def save(self):
            cur.execute(
                f"""
                    INSERT INTO {self.TABLE} VALUES
                        ('{self.name}', 
                        '{self.state}', 
                        '{self.identifier}', 
                         {self.enrolled_students}, 
                        '{self.max_enrollment}', 
                        '{self.subjects}')
                """
            )
            con.commit()

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

    student = DbStudent()
    enrollment = DbEnrollment()
    course = DbCourse()
