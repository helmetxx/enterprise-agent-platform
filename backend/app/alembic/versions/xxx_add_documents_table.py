"""add documents table

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-01-29 21:35:40.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_type', sa.String(length=100), nullable=True),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('knowledge_base_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['knowledge_base_id'], ['knowledge_bases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents') 