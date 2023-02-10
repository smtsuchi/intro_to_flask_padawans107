"""empty message

Revision ID: 8a28fc4286b9
Revises: 44cb57d7e2f5
Create Date: 2023-02-09 19:52:01.282882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a28fc4286b9'
down_revision = '44cb57d7e2f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint('likes_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('likes_post_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'post', ['post_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('likes_post_id_fkey', 'post', ['post_id'], ['id'])
        batch_op.create_foreign_key('likes_user_id_fkey', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###
