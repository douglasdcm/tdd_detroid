import os
from tests.conftest import set_database_for_tests
from src.database import Database
from src.constants import DATABASE_FILE


if __name__ == "__main__":
    try:
        os.remove(DATABASE_FILE)
    except Exception:
        pass
    set_database_for_tests(Database())
