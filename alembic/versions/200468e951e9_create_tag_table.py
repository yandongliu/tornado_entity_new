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
        'entity',
        sa.Column('uuid', sa.CHAR(length=36), primary_key=True),
        sa.Column('parent_uuid', sa.CHAR(length=36), sa.ForeignKey('entity.uuid'), nullable=False, index=True),
        sa.Column('type_', sa.String(30), nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False, index=False),
        sa.Column('created_at', sa.TIMESTAMP, index=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP, index=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'attribute',
        sa.Column('uuid', sa.CHAR(length=36), primary_key=True),
        sa.Column('type_', sa.String(30), nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False, index=False),
        sa.Column('regex', sa.String(length=36), nullable=True, index=False),
        sa.Column('created_at', sa.TIMESTAMP, index=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP, index=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'entity_attribute',
        sa.Column('uuid', sa.CHAR(length=36), primary_key=True),
        sa.Column('entity_uuid', sa.CHAR(length=36), sa.ForeignKey('entity.uuid'), nullable=False, index=True),
        sa.Column('attribute_uuid', sa.CHAR(length=36), sa.ForeignKey('attribute.uuid'), nullable=False, index=True),
        sa.Column('created_at', sa.TIMESTAMP, index=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP, index=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('entity_attribute')
    op.drop_table('attribute')
    op.drop_table('entity')
