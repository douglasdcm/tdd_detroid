from src.curso import Curso
from src.catalogo_curso import CatalogoCurso


class Coordenador:
    
    def __init__(self):            
        self._alunos = list()

    def _pega_alunos(self, curso):
        for aluno in curso.pega_lista_alunos():
            alunos = {
                    "nome": aluno.pega_nome(),
                    "materias": aluno.pega_materias_cursadas(),
                    "coeficiente rendimento": aluno.pega_coeficiente_rendimento()
                }
            self._alunos.append(alunos)
        return self._alunos

    def listar_detalhe_alunos(self, curso):          
        if isinstance(curso, list):
            for meu_curso in self._curso:            
                self._pega_alunos(meu_curso)
        if isinstance(curso, Curso):
            self._pega_alunos(curso) 
        return {"alunos": self._alunos}
