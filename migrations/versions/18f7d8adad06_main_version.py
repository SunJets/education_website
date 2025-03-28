"""main version

Revision ID: 18f7d8adad06
Revises: 
Create Date: 2025-03-22 23:53:27.210369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18f7d8adad06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('user_ref_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_ref_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_course_description'), ['description'], unique=False)
        batch_op.create_index(batch_op.f('ix_course_title'), ['title'], unique=False)
        batch_op.create_index(batch_op.f('ix_course_user_ref_id'), ['user_ref_id'], unique=False)

    op.create_table('user_course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('progress', sa.SmallInteger(), nullable=False),
    sa.Column('user_ref_id', sa.Integer(), nullable=False),
    sa.Column('course_ref_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_ref_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_ref_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user_course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_course_course_ref_id'), ['course_ref_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_course_description'), ['description'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_course_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_course_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_course_user_ref_id'), ['user_ref_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_course_user_ref_id'))
        batch_op.drop_index(batch_op.f('ix_user_course_timestamp'))
        batch_op.drop_index(batch_op.f('ix_user_course_name'))
        batch_op.drop_index(batch_op.f('ix_user_course_description'))
        batch_op.drop_index(batch_op.f('ix_user_course_course_ref_id'))

    op.drop_table('user_course')
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_course_user_ref_id'))
        batch_op.drop_index(batch_op.f('ix_course_title'))
        batch_op.drop_index(batch_op.f('ix_course_description'))

    op.drop_table('course')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
