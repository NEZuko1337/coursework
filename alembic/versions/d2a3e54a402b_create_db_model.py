"""create db model

Revision ID: d2a3e54a402b
Revises: 
Create Date: 2025-03-16 18:18:42.747319

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd2a3e54a402b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(text('CREATE EXTENSION IF NOT EXISTS pgcrypto;'))
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'investments_results',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=sa.text("gen_random_uuid()")),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('max_profit', sa.Float(), nullable=False),
        sa.Column('total_investment', sa.Float(), nullable=False),
        sa.Column('roi', sa.Float(), nullable=False),
        sa.Column('distribution', JSONB(), nullable=False),
        sa.Column('enterprise_details', JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), 
                  onupdate=sa.func.now(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('investments_results')
    # ### end Alembic commands ###
