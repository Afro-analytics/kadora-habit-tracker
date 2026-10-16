"""add completion uniqueness constraint

Revision ID: 4da736c4827c
Revises: 
Create Date: 2026-09-15 19:04:51.242008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4da736c4827c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("completions") as batch_op:
        batch_op.create_unique_constraint(
            "uq_habit_completion_date",
            ["habit_id", "completion_date"]
        )
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table("completions") as batch_op:
        batch_op.drop_constraint(
            "uq_habit_completion_date",
            type_="unique"
        )
    # ### end Alembic commands ###
