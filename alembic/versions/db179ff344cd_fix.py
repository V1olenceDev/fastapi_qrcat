"""Fix

Revision ID: db179ff344cd
Revises: bbcc3f80caf6
Create Date: 2024-03-28 21:33:18.846206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db179ff344cd'
down_revision = 'bbcc3f80caf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.alter_column('full_amount',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.alter_column('full_amount',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.alter_column('full_amount',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.alter_column('full_amount',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
