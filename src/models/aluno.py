from src.utils.sql_client import SqlClient
from src.schemes.student import AlunoBd
from src.schemes.for_association import MateriaAlunoBd
from src.models.curso import CursoModelo
from src.utils.sql_client import SqlClient
from src.utils.exceptions import ErroAluno, ErroBancoDados, ErroMateriaAluno
from src.models.materia import MateriaModelo
from src.models.curso import CursoModelo
from sqlalchemy.orm import Query


class AlunoModelo:
    def __init__(self, conn: SqlClient) -> None:
        self._conn = conn
        self._aluno_id = None

    @property
    def id(self):
        return self._aluno_id

    @id.setter
    def id(self, valor):
        self._aluno_id = valor
        self.__pega_aluno()

    def __verifica_limite_nota(self, nota):
        if nota > 10:
            raise ErroAluno("Nota não pode ser maior que 10")
        if nota < 0:
            raise ErroAluno("Nota não pode ser menor que 0")

    def lanca_nota(self, materia_id, nota):
        nota = int(nota)
        self.__verifica_limite_nota(nota)
        self.__verifica_aluno_inscrito_materia(materia_id)
        query = Query(MateriaAlunoBd).filter(
            MateriaAlunoBd.aluno_id == self._aluno_id,
            MateriaAlunoBd.materia_id == materia_id,
        )
        mas = self._conn.roda_query(query)
        mas[0].aluno_nota = nota
        self._conn.update()
        self.__calcula_coef_rend()

    def __calcula_coef_rend(self):
        mas = self.__pega_materias_aluno()
        conta = 0
        soma_nota = 0
        for ma in mas:
            if ma.aluno_nota:
                soma_nota += ma.aluno_nota
                conta += 1
        aluno = self.__pega_aluno()
        aluno.coef_rend = int(round(soma_nota / conta, 1))
        self._conn.update()

    def __pega_materias_aluno(self):
        query = Query(MateriaAlunoBd).filter(
            MateriaAlunoBd.aluno_id == self._aluno_id,
        )
        mas = self._conn.roda_query(query)
        return mas

    def __verifica_aluno_inscrito_materia(self, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == int(
                self._aluno_id
            ) and instancia.materia_id == int(materia_id):
                return
        raise ErroAluno(
            f"Aluno {self._aluno_id} não está inscrito na matéria {materia_id}"
        )

    def __pega_aluno(self):
        try:
            return self._conn.lista(AlunoBd, self._aluno_id)
        except ErroBancoDados:
            raise ErroAluno(f"Aluno {self._aluno_id} não existe")

    def __verifica_pode_inscrever_curso(self):
        aluno = self.__pega_aluno()
        if aluno.curso_id is not None:
            raise ErroAluno("Aluno esta inscrito em outro curso")

    def __verifica_minimo_3_materias(self, aluno_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        qtde_materias = 0
        for instancia in resultado:
            if instancia.aluno_id == aluno_id:
                qtde_materias += 1
            if qtde_materias >= 3:
                return
        raise ErroMateriaAluno("Aluno deve se inscrever em 3 materias no minimo")

    def __verifica_aluno_ja_inscrito_materia(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == int(aluno_id) and instancia.materia_id == int(
                materia_id
            ):
                raise ErroMateriaAluno(
                    f"Aluno {aluno_id} já está inscrito na matéria {materia_id}"
                )

    def __pega_curso_id(self):
        curso_id = self._conn.lista(AlunoBd, self.id).curso_id
        if not curso_id:
            raise ErroAluno(f"Aluno {self.id} não está inscrito em nenhum curso")
        return curso_id

    def cria(self, nome):
        nome = nome.strip()
        if len(nome) == 0:
            raise ErroAluno("Invalid student name")
        aluno = AlunoBd(nome=nome)
        self._conn.cria(aluno)
        self._aluno_id = self._conn.lista_maximo(AlunoBd).id

    def inscreve_materia(self, materia_id):
        curso_id = self.__pega_curso_id()
        MateriaModelo(self._conn).verifica_existencia(materia_id, curso_id)
        self.__verifica_aluno_ja_inscrito_materia(self._aluno_id, materia_id)
        ma = MateriaAlunoBd(aluno_id=self._aluno_id, materia_id=materia_id)
        self._conn.cria(ma)
        self.__verifica_minimo_3_materias(self._aluno_id)

    def inscreve_curso(self, curso_id):
        aluno = self.__pega_aluno()
        CursoModelo(self._conn).verifica_existencia(curso_id)
        self.__verifica_pode_inscrever_curso()
        aluno.curso_id = curso_id
        self._conn.confirma()
