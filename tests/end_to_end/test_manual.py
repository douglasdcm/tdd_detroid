from src.utils import sql_client
from src.schemes.student import StudentDB


# @mark.skip(reason="Teste manual")
def test_popula_banco_para_test_manual():
    res = sql_client.get_all(StudentDB)
    print(res)


if __name__ == "__main__":
    test_popula_banco_para_test_manual()
