import pytest
import asyncio
from pathlib import Path
from app.core.dify import dify_client
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class TestDifyDocumentUpload:
    # 使用已知的测试数据
    TEST_DATASET_ID = "9eac8a1c-5639-4818-bfeb-e6b948d9a353"
    TEST_FILE_CONTENT = """
    这是一个测试文档。
    用于测试DIFY文档上传功能。
    """

    @pytest.fixture
    def test_file(self, tmp_path):
        """创建测试文件"""
        file_path = tmp_path / "test_doc.txt"
        file_path.write_text(self.TEST_FILE_CONTENT)
        return file_path

    @pytest.mark.asyncio
    async def test_create_document(self, test_file):
        """测试上传文档到DIFY"""
        try:
            logger.info(f"开始测试上传文档到DIFY, dataset_id: {self.TEST_DATASET_ID}")
            logger.info(f"测试文件路径: {test_file}")

            response = await dify_client.create_document_by_file(
                dataset_id=self.TEST_DATASET_ID,
                file_path=str(test_file),
                file_name="test_doc.txt"
            )

            logger.info(f"DIFY响应: {response}")

            # 验证响应
            assert "document" in response
            assert "id" in response["document"]
            assert response["document"]["name"] == "test_doc.txt"
            assert response["document"]["indexing_status"] in ["waiting", "processing", "completed", "parsing"]

            return response

        except Exception as e:
            logger.error(f"测试失败: {str(e)}")
            raise

def main():
    """手动运行测试"""
    logging.basicConfig(level=logging.INFO)
    
    async def run_test():
        test = TestDifyDocumentUpload()
        
        # 使用时间戳和UUID生成唯一的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_name = f"test_doc_{timestamp}_{unique_id}.txt"
        
        # 创建临时目录和文件
        tmp_dir = Path("./tmp")
        tmp_dir.mkdir(exist_ok=True)
        test_file = tmp_dir / file_name
        
        # 写入测试内容
        test_file.write_text(TestDifyDocumentUpload.TEST_FILE_CONTENT)
        print(f"创建测试文件: {test_file}")
        
        try:
            result = await test.test_create_document(test_file)
            print("测试成功!")
            print(f"文档ID: {result['document']['id']}")
            print(f"完整响应: {result}")
            print(f"测试文件保存在: {test_file}")
        except Exception as e:
            print(f"测试失败: {e}")
            print(f"测试文件保存在: {test_file}")
            raise

    asyncio.run(run_test())

if __name__ == "__main__":
    main() 