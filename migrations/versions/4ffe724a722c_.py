"""empty message

Revision ID: 4ffe724a722c
Revises: d690cf28806a
Create Date: 2021-05-22 23:42:10.943036

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4ffe724a722c'
down_revision = 'd690cf28806a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('eval_form', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('eval_form', sa.Column('q1', sa.Boolean(), nullable=False))
    op.add_column('eval_form', sa.Column('q2', sa.Boolean(), nullable=False))
    op.add_column('eval_form', sa.Column('q3', sa.Boolean(), nullable=False))
    op.add_column('eval_form', sa.Column('q4', sa.Boolean(), nullable=False))
    op.add_column('eval_form', sa.Column('q5', sa.Boolean(), nullable=False))
    op.add_column('eval_form', sa.Column('q6', sa.Boolean(), nullable=False))
    op.add_column('eval_form', sa.Column('title', sa.String(length=20), nullable=True))
    op.create_foreign_key(None, 'eval_form', 'courses', ['title'], ['title'])
    op.drop_column('eval_form', 'question')
    op.drop_column('eval_form', 'operation')
    op.drop_column('eval_form', 'number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('eval_form', sa.Column('number', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False))
    op.add_column('eval_form', sa.Column('operation', mysql.VARCHAR(length=200), nullable=False))
    op.add_column('eval_form', sa.Column('question', mysql.VARCHAR(length=200), nullable=False))
    op.drop_constraint(None, 'eval_form', type_='foreignkey')
    op.drop_column('eval_form', 'title')
    op.drop_column('eval_form', 'q6')
    op.drop_column('eval_form', 'q5')
    op.drop_column('eval_form', 'q4')
    op.drop_column('eval_form', 'q3')
    op.drop_column('eval_form', 'q2')
    op.drop_column('eval_form', 'q1')
    op.drop_column('eval_form', 'id')
    # ### end Alembic commands ###
