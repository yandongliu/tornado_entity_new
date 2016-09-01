"""create_tag_table

Revision ID: 200468e951e9
Revises: 
Create Date: 2016-08-29 07:17:48.128720

"""

# revision identifiers, used by Alembic.
revision = '200468e951e9'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'tag',
        sa.Column('uuid', sa.CHAR(length=36), primary_key=True),
        sa.Column('tag_type', sa.String(length=36), nullable=False, index=True),
        sa.Column('tag_name', sa.String(length=36), nullable=False, index=False),
        sa.Column('value', sa.String(length=36), nullable=False, index=False),
        sa.Column('parent_uuid', sa.CHAR(length=36), sa.ForeignKey('tag.uuid'), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False, index=False),
    )


def downgrade():
    op.drop_table('tag')
