from src.utils.exceptions import CourseException
from src.utils.rest import post, get_all, get, get_by_query


class CourseStorage:
    def __init__(self) -> None:
        self._curso_id = None
        self._resources = "cursos"

    def create_course(self, nome):
        post(self._resources, {"nome": nome})
        return len(get_all("cursos"))

    def get_course(self, curso_id):
        try:
            return get(self._resources, curso_id)
        except IndexError:
            raise CourseException(f"Curso {curso_id} não existe")

    def check_exists(self, curso_id):
        self.get_course(curso_id)

    def check_name(self, name):
        if len(name.strip()) == 0:
            raise CourseException("Nome do curso invalido")

    def check_course_exists(self, name):
        res = get_by_query(self._resources, f"nome=eq.{name}")
        if len(res) > 0:
            raise CourseException(f"Existe outro curso com o nome {name}")

    def check_has_tree_courses(self):
        res = get_all(self._resources)
        if len(res) < 3:
            return
        res = get_all("view_course_and_discipline")
        if len(res) < 3:
            raise CourseException(
                "Necessários 3 cursos com 3 três matérias para se criar novos cursos"
            )
