from src import tabelas


def get_table_list():
    students = {
        "name": tabelas.students,
        "columns": [
            {"name": "name", "type": "text", "constraints": "not null"},
            {"name": "score", "type": "integer", "constraints": "not null"},
            {"name": "situation", "type": "text", "constraints": "not null"},
        ],
    }
    courses = {
        "name": tabelas.courses,
        "columns": [
            {"name": "name", "type": "text", "constraints": "not null"},
        ],
    }
    cursos = {
        "name": tabelas.cursos,
        "columns": [
            {"name": "nome", "type": "text", "constraints": "not null"},
        ],
    }
    enrolment = {
        "name": tabelas.inscricao_aluno_curso,
        "columns": [
            {"name": "aluno_id", "type": "integer", "constraints": "not null"},
            {"name": "curso_id", "type": "integer", "constraints": "not null"},
        ],
    }
    disciplines = {
        "name": tabelas.materias,
        "columns": [
            {"name": "nome", "type": "text", "constraints": "not null"},
        ],
    }
    enrol_course_discipline = {
        "name": tabelas.associa_curso_materia,
        "columns": [
            {"name": "curso_id", "type": "integer", "constraints": "not null"},
            {"name": "materia_id", "type": "integer", "constraints": "not null"},
        ],
    }
    assoc_curso_materia = {
        "name": tabelas.associa_curso_materia,
        "columns": [
            {"name": "curso_id", "type": "integer", "constraints": "not null"},
            {"name": "materia_id", "type": "integer", "constraints": "not null"},
        ],
    }
    assoc_aluno_curso = {
        "name": tabelas.inscricao_aluno_curso,
        "columns": [
            {"name": "aluno_id", "type": "integer", "constraints": "not null"},
            {"name": "curso_id", "type": "integer", "constraints": "not null"},
        ],
    }
    general_coordinator = {
        "name": tabelas.coordenador_geral,
        "columns": [
            {"name": "_", "type": "text", "constraints": "not null"},
        ],
    }

    return [
        students,
        courses,
        enrolment,
        disciplines,
        cursos,
        enrol_course_discipline,
        assoc_curso_materia,
        assoc_aluno_curso,
        general_coordinator,
    ]
