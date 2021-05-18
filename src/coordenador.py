from src.catalogo_curso import CatalogoCurso


class Coordenador:
    def __init__(self, curso=None, geral=False):  
        self._verifica_parametros(curso, geral)           
        self._alunos = list()
        self._geral = geral
        self._catalogo = CatalogoCurso()
        if geral:
                self._curso = self._catalogo.pega_cursos()
        else:
            self._curso = curso

    def _verifica_parametros(self, curso, geral):
        if geral and curso:
                raise Exception("Coordenador geral não pode especificar um curso.")

    def _pega_alunos(self, curso):
        for aluno in curso.pega_lista_alunos():
            alunos = {
                    "nome": aluno.pega_nome(),
                    "materias": aluno.pega_materias_cursadas(),
                    "coeficiente rendimento": aluno.pega_coeficiente_rendimento()
                }
            self._alunos.append(alunos)
        return self._alunos

    def listar_detalhe_alunos(self):          
        if isinstance(self._curso, list):
            for curso in self._curso:            
                self._pega_alunos(curso)
        else:
            self._pega_alunos(self._curso)        
        return {"alunos": self._alunos}
