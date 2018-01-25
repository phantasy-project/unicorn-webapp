"""empty message

Revision ID: 6da128e06c5a
Revises: 
Create Date: 2018-01-25 09:58:44.983529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6da128e06c5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=True)
    op.create_table('function',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('invoked', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=1000), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('args', sa.String(length=500), nullable=True),
    sa.Column('lastin', sa.String(length=500), nullable=True),
    sa.Column('lastout', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_function_invoked'), 'function', ['invoked'], unique=False)
    op.create_index(op.f('ix_function_name'), 'function', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_function_name'), table_name='function')
    op.drop_index(op.f('ix_function_invoked'), table_name='function')
    op.drop_table('function')
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###