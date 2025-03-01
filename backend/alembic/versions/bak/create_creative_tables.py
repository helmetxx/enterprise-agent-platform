"""create creative tables

Revision ID: 2024_01_22_01
Revises: previous_revision_id
Create Date: 2024-01-22 15:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import JSON

# revision identifiers
revision = '2024_01_22_01'
down_revision = 'previous_revision_id'  # 替换为你的上一个迁移版本ID
branch_labels = None
depends_on = None

def upgrade():
    # 创意项目表
    op.create_table(
        'creative_projects',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('enterprise_id', sa.String(36), sa.ForeignKey('enterprises.id'), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('status', sa.Enum('draft', 'in_progress', 'completed'), default='draft'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())
    )

    # 文档分析结果表
    op.create_table(
        'document_analysis',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('creative_projects.id'), nullable=False),
        sa.Column('analysis_type', sa.Enum('core_features', 'feature_relations', 'key_insights')),
        sa.Column('content', JSON),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp())
    )

    # 市场分析结果表
    op.create_table(
        'market_analysis',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('creative_projects.id'), nullable=False),
        sa.Column('analysis_data', JSON),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp())
    )

    # 创意生成结果表
    op.create_table(
        'idea_generations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('creative_projects.id'), nullable=False),
        sa.Column('idea_content', JSON),
        sa.Column('evaluation_score', sa.DECIMAL(3, 2)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp())
    )

    # 图片生成结果表
    op.create_table(
        'generated_images',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('creative_projects.id'), nullable=False),
        sa.Column('idea_id', sa.String(36), sa.ForeignKey('idea_generations.id'), nullable=False),
        sa.Column('image_url', sa.String(255)),
        sa.Column('prompt_used', sa.Text),
        sa.Column('style_config', JSON),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp())
    )

    # 方案设计结果表
    op.create_table(
        'solution_designs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('creative_projects.id'), nullable=False),
        sa.Column('technical_solution', JSON),
        sa.Column('feasibility_study', JSON),
        sa.Column('implementation_path', JSON),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp())
    )

def downgrade():
    op.drop_table('solution_designs')
    op.drop_table('generated_images')
    op.drop_table('idea_generations')
    op.drop_table('market_analysis')
    op.drop_table('document_analysis')
    op.drop_table('creative_projects') 