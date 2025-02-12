"""add columns surname and patronomic

Revision ID: 56473a7c89db
Revises: 5cd6589d94c5, a32371b1c0fd
Create Date: 2025-02-12 01:04:14.293458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56473a7c89db'
down_revision: Union[str, None] = ('5cd6589d94c5', 'a32371b1c0fd')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
