"""Initial migration

Revision ID: 5fcbcf44bd75
Revises:
Create Date: 2024-06-24 16:53:49.405838

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5fcbcf44bd75"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("satellites", schema=None) as batch_op:
        batch_op.drop_column("archive_collected")
        batch_op.drop_column("other_ids")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("satellites", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "other_ids",
                postgresql.ARRAY(sa.INTEGER()),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "archive_collected",
                sa.BOOLEAN(),
                server_default=sa.text("false"),
                autoincrement=False,
                nullable=False,
            )
        )

    # ### end Alembic commands ###