# Controle de notas de alunos de faculdadde
## Introdução
Este projeto tem o objetivo de exercitar os "code smells" relacionados a testes unitários utilizando um aplicativo que simula um negócio real.
O código será desenvolvido com a técnica TDD ao estilo Detroid, daí o nome do repositório.
O aplicativo simula o controle de notas dos alunos de uma universidade. Abaixo segue a especificação do aplicativo:
Definição de Feito (Definition of Done):
1. Testes unitários estão cobrindo a funcionalidade
2. A funcionalidade está desenvolvidade para ser utilizada via CLI
3. Os dados estão sendo salvos no banco de dados
# Entregas
Construção das funções básicas do sistema
1. Cada aluno terá um controle de notas chamado "coeficiente de rendimento" (CR)
2. O CR é a média das notas do aluno nas matérias já cursadas
3. O aluno é considerado aprovado na universidade se seu CR for acima ou igual a 7 (sete) ao final do curso
4. Caso o aluno curse a mesma matéria mais de uma vez, a maior nota será considerada no cálculo do CR
5. ~~A faculdade terá inicialmente 3 cursos com 3 matérias cada~~
6. ~~As matérias de cada curso podem ter nomes iguais, mas serão diferenciadas pelo número identificador único (niu)~~
7. O sistema deve calcular a situação do aluno levando em consideração as matérias cursadas e o total de matérias de cada curso
8. O aluno só poderá cursar matérias do seu curso
9. ~~Os cursos devem ter identificador único e nome~~
10. ~~O nome dos curso pode ser igual, mas o identificador único de cada curso deve ser diferente~~
11. Um curso não pode ter duas matérias com mesmo nome, mesmo que o niu seja diferente
12. A nota máxima de um aluno em uma matéria é 10
13. A nota mínima de um aluno em uma matéria é 0
14. O aluno pode trancar o curso e neste caso não pode atualizar suas notas ou matérias cursadas
15. O coordenador do curso pode listar os alunos, notas em cada matéria e cr dos alunos
16. O Aluno pode destrancar o curso e sua situação volta para a anterior
17. ~~Os alunos devem ter nomes~~
18. O coordenador geral pode listar de todos os curso os alunos e notas em cada matéria e cr de cada aluno
19. O coordenador do curso pode eliminar matérias e neste caso os alunos não podem atualizar suas notas nesta matéria
20. Os alunos só podem atualizar suas notas na matérias em que estão inscritos
21. O nome dos cursos e materias tem que ter no máximo 10 letras
22. Os cursos podem ter nomes iguais se forem de unidades diferentes
23. O aluno só pode se increver em um curso
24. O coordenador pode ser corrdenador de mais de um curso
25. O coordenador pode listar os alunos, materias e notas, e crs de todos os seus cursos (coordenador de mais de um curso)
26. O curso pode ser cancelado
27. Os cursos cancelados não podem aceitar incrições de alunos
28. Os cursos cancelados não pode ter coordenadores
29. Cada matéria pode ter no máximo 30 alunos inscritos
30. O aluno tem que se inscrever em 3 matérias no mínimo
31. Caso o número de matérias faltantes de um aluno seja menor do que 3, ele pode se inscrever em 1 matéria
32. Caso o aluno não se increva no número mínimo de matérias por semestre, ele será automaticamente reprovado
33. O aluno deve ter CPF validado no sistema externo de validação de CPFs (sistema do governo)
34. Adicionar o nome do curso nos relatórios dos coordenadores
35. O Aluno só é aprovado se tirar a nota mínima em todas as matérias do curso, mesmo se seu cr seja acima do mínimo
36. O usuário deve ser capaz de criar alunos com informações básicas
37. O usuário deve ser capaz de inscrever o aluno em um curso
38. O usuário deve ser capaz de criar cursos com o número mínimo de matérias
39. O adminstrador e somente ele deve ser capaz de listar todos os alunos com informações detalhadas (todas as informações disponíveis)
40. O admnistrador e somente ele deve ser capaz de listar todos os cursos com todas as informações disponíveis
41. O administrador e somente ele deve ser capaz de listar a relação de alunos por curso
42. O administrador e somente ele deve ser capaz de listar a relação de matérias por aluno
43. O aluno deve ser capaz de listar todas as matérias somente de seu curso
44. O aluno deve ser capaz de listar todas as suas matérias cursadas
45. O aludo deve ser capaz de listar as matérias faltantes
46. O administrador deve ser capaz se listar todos os coordenadores de cursos com as informação disponíveisop
47. O aluno tem 10 semestres para se formar
48. Caso o aluno exceda os 10 semestres, ele é automaticamente reprovado
49. O coordenador só pode ser coordenador de 3 cursos no máximo
50. O coordenador geral não pode ser coordenador de cursos