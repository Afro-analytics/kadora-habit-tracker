"""add habit created_at

Revision ID: 1aa3906804ec
Revises: 4da736c4827c
Create Date: 2026-09-25 14:16:49.825941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1aa3906804ec'
down_revision: Union[str, Sequence[str], None] = '4da736c4827c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("habits") as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_column("completed")

    op.execute(
        "UPDATE habits SET created_at = CURRENT_TIMESTAMP "
        "WHERE created_at IS NULL"
    )

    with op.batch_alter_table("habits") as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=False
        )


def downgrade() -> None:
    with op.batch_alter_table("habits") as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),
            nullable=True
        )

        batch_op.add_column(
            sa.Column("completed", sa.Boolean(), nullable=True)
        )

        batch_op.drop_column("created_at")
    # ### end Alembic commands ###
