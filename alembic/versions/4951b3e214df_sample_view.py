"""sample_view

Revision ID: 4951b3e214df
Revises: ce2b8c6b5676
Create Date: 2022-10-20 11:11:41.115830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4951b3e214df'
down_revision = 'ce2b8c6b5676'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create view sample_view as
        select accession 
        from samples 
        where status = 'available'
        order by collection_date desc
        fetch first 10 rows only
        """
    )


def downgrade() -> None:
    op.execute("drop view sample_view")
