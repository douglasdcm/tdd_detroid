from src.utils.sql_client import SqlClient
from src.schemes.student import StudentDB


def test_context_conn():
    client = SqlClient("localhost")
    with client.db_session() as conn:
        conn.add(StudentDB(nome="context_std"))
        conn.commit()
        res = conn.query(StudentDB).all()
        print("res", res[0].nome)
        assert res[0].nome == "context_std"
