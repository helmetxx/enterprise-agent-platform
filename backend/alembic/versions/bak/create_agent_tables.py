"""create agent tables

Revision ID: 2025_01_26_01
Revises: None
Create Date: 2025-01-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2025_01_26_01'
down_revision = None  # 第一个迁移文件，没有前置依赖
branch_labels = None
depends_on = None

def upgrade():
    # 创建智能体表
    op.create_table(
        'agents',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('icon', sa.String(255)),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('capabilities', sa.JSON),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('version', sa.String(20)),
        sa.Column('sort_order', sa.Integer, default=0),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # 创建用户智能体使用记录表
    op.create_table(
        'agent_usage_records',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('agent_id', sa.String(36), sa.ForeignKey('agents.id'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        
        # 添加索引
        sa.Index('idx_user_agent_usage', 'user_id', 'agent_id', 'created_at')
    )

def downgrade():
    op.drop_table('agent_usage_records')
    op.drop_table('agents') 