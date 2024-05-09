import os
from src.database import Database
from src.constants import DATABASE_FILE, MAX_ENROLLMENT_TO_SUBJECT


if __name__ == "__main__":
    try:
        os.remove(DATABASE_FILE)
    except Exception:
        pass
    db = Database()

    for i in range(MAX_ENROLLMENT_TO_SUBJECT):
        db.enrollment.populate(f"student{i}", "098.765.432.12", "adm")
    db.course.populate("adm", subjects="")
    db.semester.populate("1234-1", "open")
