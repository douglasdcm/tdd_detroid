"""adiciona coluna alunos.course_id

Revision ID: 4d1381e1a05a
Revises: 56415884d069
Create Date: 2022-11-18 23:15:53.703048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4d1381e1a05a"
down_revision = "56415884d069"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.drop_table("courses")
        op.drop_table("alunos")
        op.drop_table("materias")
    except Exception:
        pass

    # ### end Alembic commands ###
    downgrade()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.drop_table("courses")
        op.drop_table("alunos")
        op.drop_table("materias")
    except Exception:
        pass

    op.create_table(
        "courses",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "alunos",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("coef_rend", sa.INTEGER(), nullable=True),
        sa.Column("course_id", sa.INTEGER(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "materias",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("course_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["courses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###
