# Controle de notas
## Introdução
Este projeto tem o objetivo de exercitar os "code smells" relacionados a testes unitários utilizando um aplicativo que simula um negócio real.
O aplicativo simula o controle de notas dos alunos de uma universidade. Abaixo segue a especificação do aplicativo:
<br>
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
## Entrega 5
1. O aluno pode trancar o curso e neste caso não pode atualizar suas notas ou matérias cursadas
2. O coordenador do curso pode listar os alunos, notas em cada matéria e cr dos alunos
## Entrega 6
3. O coordenador geral pode listar de todos os curso os alunos e notas em cada matéria e cr de cada aluno
## Entrega 7
1. O coordenador do curso pode eleminar matérias e neste caso os alunos não podem atualizar suas notas nesta matéria
## Os alunos só podem atualizar suas notas na matérias em que estão inscritos
## Entrega 8
1. O nome dos cursos e materias tem que ter no máximo 10 letras
2. Os cursos podem ter nomes iguais se forem de unidades diferentes
