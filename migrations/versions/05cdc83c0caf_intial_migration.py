"""Intial Migration

Revision ID: 05cdc83c0caf
Revises: 
Create Date: 2024-03-12 10:09:36.679344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05cdc83c0caf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('company', sa.String(length=100), nullable=True),
    sa.Column('sex', sa.String(length=1), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_info_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_info_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_info_token'), ['token'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_info_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_info_username'))
        batch_op.drop_index(batch_op.f('ix_user_info_token'))
        batch_op.drop_index(batch_op.f('ix_user_info_timestamp'))
        batch_op.drop_index(batch_op.f('ix_user_info_email'))

    op.drop_table('user_info')
    op.drop_table('role')
    op.drop_table('contact')
    # ### end Alembic commands ###
