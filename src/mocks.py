SUBJECT = "any"
SUBJECT_MAX_ENROLL = 10
COURSE = "any"
SUBJECT_STATE = "active"


class Database:
    class DbStudent:
        name = None
        state = None
        cpf = None
        identifier = None
        gpa = None
        subjects = None
        course = None

        def save(self):
            pass

        def load(self, identifier):
            self.name = "any"
            self.state = "enrolled"
            self.identifier = "any"
            self.course = "any"

    class DbEnrollment:
        def select(self, identifier):
            # NAME any, CPF 123.456.789-10, COURSE any
            DEFAULT = "290f2113c2e6579c8bb6ec395ea56572"
            if identifier == DEFAULT:
                return True
            return False

    class DbCourse:
        name = None
        state = None
        identifier = None
        enrolled_students = None
        max_enrollment = None
        subjects = None

        def save(self):
            pass

        def load_from_database(self, course_identifier):
            self.name = "any"
            self.state = "active"
            self.identifier = None
            self.enrolled_students = []
            self.max_enrollment = None
            self.subjects = ["any1", "any2", "any3"]

        def select(self, course_identifier):
            return "anything not None"

    class DbSubject:
        name = None
        state = None
        enrolled_students = None
        max_enrollment = None
        identifier = None
        course = None

        def load(self, course_identifier):
            self.name = SUBJECT
            self.state = SUBJECT_STATE
            self.identifier = None
            self.enrolled_students = []
            self.max_enrollment = SUBJECT_MAX_ENROLL
            self.course = COURSE

        def save(self):
            pass

    student = DbStudent()
    enrollment = DbEnrollment()
    course = DbCourse()
    subject = DbSubject()
