import os
import pytest
from app.services.report_service import ReportService
import requests

# 跳过实际 API 调用的测试，除非明确指定
pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_EXTERNAL_API_TESTS") != "1",
    reason="需要设置 RUN_EXTERNAL_API_TESTS=1 环境变量来运行外部 API 测试"
)

def test_export_report():
    """测试报表导出功能"""
    try:
        # 导出报表
        content = ReportService.export_report(
            identity="MRCWBG",
            format_type="PDF",
            parameters={"bizDate": "2025-03-02"}
        )
        
        # 验证返回的内容不为空
        assert content is not None
        assert len(content) > 0
        
        # 验证内容是 PDF（以 %PDF 开头）
        assert content.startswith(b'%PDF')
        
    except requests.RequestException as e:
        pytest.skip(f"外部 API 调用失败: {e}")


def test_export_report_with_save():
    """测试报表导出并保存到文件"""
    import tempfile
    
    try:
        # 创建临时文件
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        
        try:
            # 导出报表并保存
            content = ReportService.export_report(
                identity="MRCWBG",
                format_type="PDF",
                parameters={"bizDate": "2025-03-02"},
                save_path=temp_path
            )
            
            # 验证文件存在且不为空
            assert os.path.exists(temp_path)
            assert os.path.getsize(temp_path) > 0
            
            # 验证文件内容与返回内容相同
            with open(temp_path, 'rb') as f:
                file_content = f.read()
            assert file_content == content
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except requests.RequestException as e:
        pytest.skip(f"外部 API 调用失败: {e}") 