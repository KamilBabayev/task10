"""empty message

Revision ID: 08eab26a187c
Revises: 502ee430d01a
Create Date: 2024-03-22 16:23:42.999895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08eab26a187c'
down_revision = '502ee430d01a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.Enum('OPEN', 'IN_PROGRESS', 'DONE'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.Enum('OPEN', 'IN_PROGRESS', 'DONE'),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
