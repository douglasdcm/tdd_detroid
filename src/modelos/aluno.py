from src.utils.sql_client import SqlClient
from src.esquemas.aluno import AlunoBd
from src.esquemas.para_associacao import MateriaAlunoBd
from src.modelos.curso import CursoModelo
from src.utils.sql_client import SqlClient
from src.utils.exceptions import ErroAluno, ErroBancoDados, ErroMateriaAluno


class AlunoModelo:
    def __init__(self, conn: SqlClient, aluno_id=None) -> None:
        self._conn = conn
        self._aluno_id = aluno_id
        if self._aluno_id:
            self.__verifica_existencia()

    @property
    def id(self):
        return self._aluno_id

    def __verifica_existencia(self):
        try:
            self._conn.lista(AlunoBd, self._aluno_id)
        except ErroBancoDados:
            raise ErroAluno(f"Aluno {self._aluno_id} nao existe")

    def __pega_aluno(self):
        try:
            aluno = self._conn.lista(AlunoBd, self._aluno_id)
            if aluno:
                return aluno
        except ErroBancoDados:
            raise ErroAluno(f"Aluno {self._aluno_id} nao existe")

    def __verifica_pode_inscrever_curso(self):
        aluno = self.__pega_aluno()
        if aluno.curso_id is not None:
            raise ErroAluno("Aluno esta inscrito em outro curso")

    def __verifica_minimo_3_materias(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        count = 0
        for instancia in resultado:
            if instancia.aluno_id == aluno_id and instancia.materia_id == materia_id:
                count += 1
        if count < 3:
            raise ErroMateriaAluno("Aluno deve se inscrever em 3 materias no minimo")

    def __verifica_aluno_inscrito_materia(self, aluno_id, materia_id):
        resultado = self._conn.lista_tudo(MateriaAlunoBd)
        for instancia in resultado:
            if instancia.aluno_id == aluno_id and instancia.materia_id == materia_id:
                raise ErroMateriaAluno(
                    f"Aluno {aluno_id} ja esta inscrito na materia {materia_id}"
                )

    def cria(self, nome):
        aluno = AlunoBd(nome=nome)
        self._conn.cria(aluno)
        self._aluno_id = self._conn.lista_maximo(AlunoBd).id

    def inscreve_materia(self, materia_id):
        self.__verifica_aluno_inscrito_materia(self._aluno_id, materia_id)
        ma = MateriaAlunoBd(aluno_id=self._aluno_id, materia_id=materia_id)
        self._conn.cria(ma)
        self.__verifica_minimo_3_materias(self._aluno_id, materia_id)

    def inscreve_curso(self, curso_id):
        aluno = self.__pega_aluno()
        CursoModelo(self._conn, curso_id)
        self.__verifica_pode_inscrever_curso()
        aluno.curso_id = curso_id
        self._conn.confirma()
