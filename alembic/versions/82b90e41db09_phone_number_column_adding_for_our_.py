"""phone number column adding for our users table

Revision ID: 82b90e41db09
Revises: 
Create Date: 2026-10-11 22:19:51.131695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82b90e41db09'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column('users',sa.Column('phone_number',sa.String(20),nullable=True))

def downgrade() -> None:
   # op.drop_column('users', 'phone_number')
   op.drop_column('users','phone_number')
