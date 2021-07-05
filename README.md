# Controle de notas de alunos de faculdadde
## Introdução
Este projeto tem o objetivo de exercitar os "code smells" relacionados a testes unitários utilizando um aplicativo que simula um negócio real.
O código será desenvolvido com a técnica TDD ao estilo Detroid, daí o nome do repositório.
O aplicativo simula o controle de notas dos alunos de uma universidade. Abaixo segue a especificação do aplicativo:
# Fase 1
Construção das funções básicas do sistema
## Entrega 1 - finalizada
1. Cada aluno terá um controle de notas chamado "coeficiente de rendimento" (CR)
2. O CR é a média das notas do aluno nas disciplinas já cursadas
3. O aluno é considerado aprovado na universidade se seu CR for acima ou igual a 7 (sete) ao final do curso
4. Caso o aluno curse a mesma matéria mais de uma vez, a maior nota será considerada no cálculo do CR
## Entrega 2 - finalizada
1. A faculdade terá inicialmente 3 cursos com 3 matérias cada
2. As matérias de cada curso podem ter nomes iguais, mas serão diferenciadas pelo número identificador único (niu)
## Entrega 3 - finalizado
1. O sistema deve calcular a situação do aluno levando em consideração as matérias cursadas e o total de matérias de cada curso
2. O aluno só poderá cursar matérias do seu curso
3. Os cursos devem ter identificador único e nome
4. O nome dos curso pode ser igual, mas o identificador único de cada curso deve ser diferente
5. Um curso não pode ter duas matérias com mesmo nome, mesmo que o niu seja diferente
## Entrega 4 - finalizado
1. A nota máxima de um aluno em uma matéria é 10
2. A nota mínima de um aluno em uma matéria é 0
## Entrega 5 - finalizado
1. O aluno pode trancar o curso e neste caso não pode atualizar suas notas ou matérias cursadas
2. O coordenador do curso pode listar os alunos, notas em cada matéria e cr dos alunos
3. O Aluno pode destrancar o curso e sua situação volta para a anterior
4. Os alunos devem ter nomes
## Entrega 6 - finalizado
3. O coordenador geral pode listar de todos os curso os alunos e notas em cada matéria e cr de cada aluno
## Entrega 7
1. O coordenador do curso pode eliminar matérias e neste caso os alunos não podem atualizar suas notas nesta matéria
2. Os alunos só podem atualizar suas notas na matérias em que estão inscritos
## Entrega 8 - finalizado
1. O nome dos cursos e materias tem que ter no máximo 10 letras
2. Os cursos podem ter nomes iguais se forem de unidades diferentes
## Entrega 9
1. O aluno só pode se increver em um curso
2. O coordenador pode ser corrdenador de mais de um curso
3. O coordenador pode listar os alunos, materias e notas, e crs de todos os seus cursos (coordenador de mais de um curso)
## Entrega 10
1. O curso pode ser cancelado
2. Os cursos cancelados não podem aceitar increições de alunos
3. Os cursos cancelados não pode ter coordenadores
## Entrega 11
1. O coordenador só pode ser coordenador de 3 cursos no máximo
2. O coordenador geral não pode ser coordenador de cursos
## Entrega 12
1. O aluno tem 10 semetres para se formar
2. Caso o aluno exceda os 10 semestres, ele é automaticamente reprovado
## Entrega 13
1. Cada matéria pode ter no máximo 30 alunos inscritos
2. O aluno tem que se inscrever em 3 matérias no mínimo
3. Caso o número de matérias faltantes de um aluno seja menor do que 3, ele pode se inscrever em 1 matéria
## Entrega 14
1. Caso o aluno não se increva no número mínimo de matérias por semestre, ele será automaticamente reprovado
## Entrega 15
1. O aluno deve ter CPF validado no sistema externo de validação de CPFs (sistema do governo)
## Entrega 16
1. Adicionar o nome do curso nos relatórios dos coordenadores
## Entrega 17
1. O Aluno só é aprovado se tirar a nota mínima em todas as matérias do curso, mesmo se seu cr seja acima do mínimo
# Fase 2
Construção da interface de comandos 
## Entrega 1 - fianlizada
1. O usuário deve ser capaz de criar alunos com informações básicas
## Entrega 2
1. O usuário deve ser capaz de inscrever o aluno em um curso
2. O usuário deve ser capaz de criar cursos com o número mínimo de matérias
## Entrega 3
1. O adminstrador deve ser capaz de listar todos os alunos com informações detalhas (toas as informações disponíveis)
2. O admnistrador deve ser capaz de listar todos os cursos com todas as informações disponíveis
3. O administrador e somente ele deve ser capaz de listar a relação de alunos por curso
4. O administrador e somente ele deve ser capaz de listar a relação de matérias por aluno
## Entrega 4
1. O aluno deve ser capaz de listar todas as matérias de seu curso
2. O aluno deve ser capaz de listar todas as suas matérias cursadas
3. O aludo deve ser capaz de listar as matérias faltantes
## Entrega 5
1. O administrador deve ser capaz se listar todos os coordenadores de cursos com as informação disponíveis