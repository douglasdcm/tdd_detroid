"""adiciona coluna aluno_nota em materia_aluno

Revision ID: a00e45c8086b
Revises: aff28b5a130a
Create Date: 2022-11-29 21:49:38.905376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a00e45c8086b"
down_revision = "aff28b5a130a"
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.drop_table("materia_aluno")
    except Exception:
        pass
    op.create_table(
        "materia_aluno",
        sa.Column("aluno_nota", sa.INTEGER(), nullable=True),
        sa.Column("materia_id", sa.INTEGER(), nullable=True),
        sa.Column("student_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["materia_id"],
            ["materias.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["alunos.id"],
        ),
    )


def downgrade():
    try:
        op.drop_table("materia_aluno")
    except Exception:
        pass
    op.create_table(
        "materia_aluno",
        sa.Column("materia_id", sa.INTEGER(), nullable=True),
        sa.Column("student_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["materia_id"],
            ["materias.id"],
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["alunos.id"],
        ),
    )
