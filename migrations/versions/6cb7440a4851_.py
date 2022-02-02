"""empty message

Revision ID: 6cb7440a4851
Revises: 2dc1b76a83ab
Create Date: 2021-04-15 16:58:19.462513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cb7440a4851'
down_revision = '2dc1b76a83ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('team', table_name='pa_qresponse')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('team', 'pa_qresponse', ['team'], unique=True)
    # ### end Alembic commands ###