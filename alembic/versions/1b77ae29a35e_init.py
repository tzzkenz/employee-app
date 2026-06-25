"""init

Revision ID: 1b77ae29a35e
Revises: 431cdc5ab891
Create Date: 2026-06-10 14:17:31.273780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b77ae29a35e'
down_revision: Union[str, Sequence[str], None] = '431cdc5ab891'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


status_enum = sa.Enum(
    'ACTIVE',
    'INACTIVE',
    'PROBATION',
    name='employeestatus'
)

def upgrade() -> None:
    # 1. Create ENUM type explicitly
    status_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add column using it
    op.add_column(
        'employees',
        sa.Column(
            'status',
            status_enum,
            nullable=True,
            server_default=sa.text("'PROBATION'")
        )
    )

    # 3. Backfill
    op.execute("""
        UPDATE employees
        SET status = 'PROBATION'
        WHERE status IS NULL
    """)

    # 4. Enforce NOT NULL
    op.alter_column('employees', 'status', nullable=False)

    # Optional: remove default if you don’t want implicit fallback
    op.alter_column('employees', 'status', server_default=None)


def downgrade() -> None:
    op.drop_column('employees', 'status')

    # Drop ENUM type (Postgres only)
    status_enum.drop(op.get_bind(), checkfirst=True)