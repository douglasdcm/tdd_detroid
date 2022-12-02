"""first autogenerated

Revision ID: f5e1be582417
Revises: 
Create Date: 2022-11-18 22:47:42.815378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f5e1be582417"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.drop_table("cursos")
        op.drop_table("alunos")
        op.drop_table("materias")
    except Exception:
        pass
    # ### end Alembic commands ###
    downgrade()


def downgrade():
    try:
        op.drop_table("cursos")
        op.drop_table("alunos")
        op.drop_table("materias")
    except Exception:
        pass
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "materias",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("nome", sa.VARCHAR(), nullable=True),
        sa.Column("curso", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["curso"],
            ["cursos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "alunos",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("nome", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cursos",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("nome", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###