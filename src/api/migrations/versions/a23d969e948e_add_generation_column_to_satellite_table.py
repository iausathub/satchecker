"""Add generation column to Satellite table

Revision ID: a23d969e948e
Revises: d99ee9e842ed
Create Date: 2025-04-14 11:24:19.081853

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a23d969e948e"
down_revision = "d99ee9e842ed"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("satellites", sa.Column("generation", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("satellites", "generation")
