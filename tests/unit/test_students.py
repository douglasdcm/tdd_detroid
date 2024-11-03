from src.schemes.for_association import MateriaAlunoBd
from src.schemes.student import AlunoBd
from src.models.aluno import AlunoModelo
from src.models.aluno import ErroAluno
from src.utils.exceptions import (
    ErroAluno,
    ErroMateriaAluno,
    ErroMateria,
    ErroCurso,
)
from tests.config import conn
from pytest import raises, mark


@mark.parametrize("input", [(""), ("   ")])
def test_student_name_cannot_be_empty(popula_banco_dados, input):
    with raises(ErroAluno, match="Invalid student name"):
        AlunoModelo(conn).cria(nome=input)


def test_arredonda_o_cr_a_uma_casa_decimal(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    aluno.lanca_nota(materia_id=1, nota=2)
    aluno.lanca_nota(materia_id=2, nota=2)
    aluno.lanca_nota(materia_id=3, nota=3)
    aluno_bd = conn.lista(AlunoBd, aluno_id)
    assert aluno_bd.coef_rend == 2.3


def test_calcula_cr_aluno_como_media_simples_das_notas_lancadas(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    aluno.lanca_nota(materia_id=1, nota=1)
    aluno.lanca_nota(materia_id=2, nota=2)
    aluno.lanca_nota(materia_id=3, nota=3)
    aluno_bd = conn.lista(AlunoBd, aluno_id)
    assert aluno_bd.coef_rend == 2


def test_lanca_nota_se_aluno_existe(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    materia_id = 1
    nota = 7
    assert aluno.lanca_nota(materia_id, nota) is None


def test_assume_maior_nota_se_duplo_lancamento_de_notas(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    materia_id = 1
    nota = 7
    nota_bd = None
    aluno.lanca_nota(materia_id, nota=nota + 1)
    aluno.lanca_nota(materia_id, nota=nota)
    mas = conn.lista_tudo(MateriaAlunoBd)
    for ma in mas:
        if ma.aluno_id == aluno_id and ma.materia_id == materia_id:
            nota_bd = ma.aluno_nota
            break
    assert nota == nota_bd


def test_nao_lanca_nota_se_menor_que_zero():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    materia_id = 1
    with raises(ErroAluno, match=f"Nota não pode ser menor que 0"):
        aluno.lanca_nota(materia_id, nota=-1)


def test_nao_lanca_nota_se_maoir_que_10():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    materia_id = 1
    with raises(ErroAluno, match=f"Nota não pode ser maior que 10"):
        aluno.lanca_nota(materia_id, nota=11)


def test_nao_lanca_nota_se_aluno_nao_inscrito_materia():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    aluno_id = aluno.id
    materia_id = 1
    with raises(
        ErroAluno, match=f"Aluno {aluno_id} não está inscrito na matéria {materia_id}"
    ):
        aluno.lanca_nota(materia_id, nota=5)


def test_lanca_notas_se_aluno_inscrito_materia(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    aluno.lanca_nota(materia_id=1, nota=5)
    assert conn.lista(AlunoBd, aluno_id).coef_rend == 5.0


def test_nao_inscreeve_aluno_se_curso_nao_existe():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    with raises(ErroAluno, match="Aluno 1 não está inscrito em nenhum curso"):
        aluno.inscreve_materia(1)


def test_mensagem_sobre_3_materias_para_apos_inscricao_em_3_materias(
    popula_banco_dados,
):

    aluno = AlunoModelo(conn)
    aluno.cria("any")
    aluno.inscreve_curso(curso_id=1)
    aluno.inscreve_materia(1)
    aluno.inscreve_materia(2)
    aluno.inscreve_materia(3)


def test_aluno_nao_pode_se_inscrever_em_materia_inexistente(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    with raises(ErroMateriaAluno):
        aluno.inscreve_materia(1)
        aluno.inscreve_materia(2)
        aluno.inscreve_materia(3)
    with raises(ErroMateria, match="Matéria 42 não existe"):
        aluno.inscreve_materia(42)


def test_aluno_nao_pode_se_inscrever_duas_vezes_na_mesma_materia(popula_banco_dados):
    aluno_id = len(conn.lista_tudo(AlunoBd))
    aluno = AlunoModelo(conn)
    aluno.id = aluno_id
    with raises(ErroMateriaAluno):
        aluno.inscreve_materia(1)
        aluno.inscreve_materia(2)
        aluno.inscreve_materia(3)
    with raises(ErroMateriaAluno, match="Aluno 1 já está inscrito na matéria 1"):
        aluno.inscreve_materia(1)


def test_inscreve_aluno_numa_materia(popula_banco_dados):
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    aluno.inscreve_curso(curso_id=1)
    actual = aluno.inscreve_materia(1)
    assert actual == "Aluno deve se inscrever em 3 materias no minimo"


def test_aluno_cria():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    assert conn.lista(AlunoBd, 1).nome == "any"
    assert conn.lista(AlunoBd, 1).id == 1


def test_inscreve_aluno_se_curso_existe():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    with raises(Exception):
        with raises(ErroCurso, match="Curso 42 nao existe"):
            aluno.inscreve_curso(curso_id=42)


def test_inscreve_aluno_curso(popula_banco_dados):
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    aluno.inscreve_curso(curso_id=1)
    assert conn.lista(AlunoBd, 1).curso_id == 1


def test_verifica_aluno_existe():
    aluno = AlunoModelo(conn)
    with raises(ErroAluno, match="Aluno 42 não existe"):
        aluno.id = 42


def test_nao_inscreve_aluno_se_curso_nao_existe():
    aluno = AlunoModelo(conn)
    aluno.cria("any")
    with raises(ErroAluno, match="Curso 42 não existe"):
        aluno.inscreve_curso(42)


def test_alunos_lista_por_id():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    aluno.cria(nome="other")
    assert conn.lista(AlunoBd, id_=2).nome == "other"


def test_alunos_lista_tudo():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    aluno.cria(nome="other")
    assert len(conn.lista_tudo(AlunoBd)) == 2


def test_alunos_cria_banco_dados():
    aluno = AlunoModelo(conn)
    aluno.cria(nome="any")
    assert conn.lista(AlunoBd, id_=1).nome == "any"
