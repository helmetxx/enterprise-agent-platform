import pytest
import asyncio
from app.core.dify import DifyClient, dify_client
from unittest.mock import patch, MagicMock

class MockDifyClient(DifyClient):
    """Mock DIFY API 客户端，用于测试"""
    async def create_knowledge_base(self, name: str, description: str = None) -> dict:
        """模拟创建知识库的响应"""
        print(f"Mock: Creating knowledge base with name: {name}, description: {description}")
        print(f"Mock: Using API URL: {self.base_url}")
        print(f"Mock: Headers: {self.headers}")
        
        # 模拟成功响应
        return {
            "id": "mock-kb-123",
            "name": name,
            "description": description,
            "status": "success"
        }

@pytest.mark.asyncio
async def test_create_knowledge_base():
    """测试创建知识库"""
    # 使用 Mock 客户端
    mock_client = MockDifyClient()
    
    # 测试创建知识库
    result = await mock_client.create_knowledge_base(
        name="Test KB",
        description="Test Description"
    )
    
    assert result["id"] == "mock-kb-123"
    assert result["name"] == "Test KB"

@pytest.mark.asyncio
async def test_real_dify_client():
    """测试真实的 DIFY API 调用"""
    try:
        result = await dify_client.create_knowledge_base(
            name="Test KB",
            description="Test Description"
        )
        print(f"Success! Created knowledge base: {result}")
    except Exception as e:
        print(f"Error creating knowledge base: {str(e)}")
        print(f"Error type: {type(e)}")
        raise

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_real_dify_client()) 