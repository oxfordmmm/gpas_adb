"""Added site tables

Revision ID: 2d2faa4c55f8
Revises: 
Create Date: 2022-06-29 15:58:47.144898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d2faa4c55f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SITES',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, on_null=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('URL', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('SITE_URL_FIELDS',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, on_null=True), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.Column('Key', sa.String(length=20), nullable=False),
    sa.Column('value', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['site_id'], ['SITES.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('SITE_URL_FIELDS')
    op.drop_table('SITES')
    # ### end Alembic commands ###
