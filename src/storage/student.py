from src.utils.exceptions import ErroAluno, ErroMateriaAluno
from src.utils.rest import get, get_by_query, get_all, patch, post
from src.utils.parser import parse_discipine_student, parse_student


class StudentStorage:
    def __init__(self):
        self._resources = "alunos"

    def subcribe_in_course(self, student_id, course_id):
        patch(self._resources, student_id, {"curso_id": course_id})

    async def get_student(self, aluno_id):
        try:
            res = await get(self._resources, aluno_id)
            return parse_student(res)
        except IndexError:
            raise ErroAluno(f"Aluno {aluno_id} não existe")

    def __get_disciplines_of_student(self, aluno_id):
        res = get_by_query("materia_aluno", query=f"aluno_id=eq.{aluno_id}")
        outcome = []
        for r in res:
            materia_aluno = parse_discipine_student(r)
            outcome.append(materia_aluno)
        return outcome

    def get_course_id(self, student_id):
        curso_id = get(self._resources, student_id).get("curso_id")
        if not curso_id:
            raise ErroAluno(f"Aluno {student_id} não está inscrito em nenhum curso")
        return curso_id

    def check_student_in_tree_disciplines(self, aluno_id):
        result = get_by_query("materia_aluno", query=f"aluno_id=eq.{aluno_id}")
        if len(result) >= 3:
            return
        raise ErroMateriaAluno("Aluno deve se inscrever em 3 materias no minimo")

    def check_student_already_in_discipline(self, aluno_id, materia_id):
        result = get_by_query(
            "materia_aluno", f"and=(aluno_id.eq.{aluno_id}, materia_id.eq.{materia_id})"
        )
        if result:
            raise ErroMateriaAluno(
                f"Aluno {aluno_id} já está inscrito na matéria {materia_id}"
            )

    async def get_maximum_id(self):
        # return len(await get_all(self._resources))
        return await get_all(self._resources)

    async def create(self, nome):
        return await post(self._resources, {"nome": nome})

    def calculate_coef_rend(self, aluno_id):
        mas = self.__get_disciplines_of_student(aluno_id)
        conta = 0
        soma_nota = 0
        for ma in mas:
            if ma.aluno_nota:
                soma_nota += ma.aluno_nota
                conta += 1
        # aluno.coef_rend = int(round(soma_nota / conta, 1))
        coef_rend = int(round(soma_nota / conta, 1))
        patch(self._resources, aluno_id, {"coef_rend": coef_rend})

    def update_grade(self, aluno_id, materia_id, grade):
        resources = "materia_aluno"
        res = get_by_query(
            resources, f"and=(aluno_id.eq.{aluno_id}, materia_id.eq.{materia_id})"
        )[0]
        id_ = parse_discipine_student(res).id
        patch(resources, id_, {"aluno_nota": grade})

    def subscribe_in_discipline(self, aluno_id, materia_id):
        post("materia_aluno", {"aluno_id": aluno_id, "materia_id": materia_id})

    def can_subscribe_course(self, aluno_id):
        aluno = self.get_student(aluno_id)
        if aluno.curso_id is not None:
            raise ErroAluno("Aluno esta inscrito em outro curso")

    def check_student_in_discipline(self, aluno_id, materia_id):
        try:
            get_by_query(
                "materia_aluno",
                f"and=(aluno_id.eq.{aluno_id}, materia_id.eq.{materia_id})",
            )[0]
        except IndexError:
            raise ErroAluno(
                f"Aluno {aluno_id} não está inscrito na matéria {materia_id}"
            )
