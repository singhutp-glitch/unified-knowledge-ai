"""add full text search

Revision ID: 1ee30c51a8f9
Revises: 94c19697ab7a
Create Date: 2026-09-05 09:56:26.052464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ee30c51a8f9'
down_revision: Union[str, Sequence[str], None] = '94c19697ab7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""
        ALTER TABLE "chunks"
        ADD COLUMN "search_vector" tsvector
        GENERATED ALWAYS AS (
            to_tsvector(
                'english',
                coalesce("section_heading", '') || ' ' ||
                coalesce("text", '')
            )
        ) STORED
    """)

    op.execute("""
        CREATE INDEX "chunk_search_vector_idx"
        ON "chunks"
        USING GIN ("search_vector")
    """)


def downgrade() -> None:
    op.execute("""
        DROP INDEX IF EXISTS "chunk_search_vector_idx"
    """)

    op.execute("""
        ALTER TABLE "chunks"
        DROP COLUMN IF EXISTS "search_vector"
    """)