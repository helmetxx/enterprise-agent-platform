import pytest
import os
from app.utils.pdf_generator import PDFGenerator
from datetime import datetime
import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

logger = logging.getLogger(__name__)

class TestPDFGenerator:
    @pytest.fixture
    def pdf_generator(self):
        return PDFGenerator()
    
    @pytest.fixture
    def test_data(self):
        # 使用本地测试图片
        test_image_path = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'test_image.png'
        )
        
        # 确保测试图片存在
        if not os.path.exists(test_image_path):
            raise FileNotFoundError(f"Test image not found: {test_image_path}")
        
        return {
            "filename": "Test Product Plan",
            "product_requirements": """
            Product Requirements:
            1. Implement auto-reply function
            2. Support multi-channel integration
            3. Provide data analysis
            """,
            "product_features": """
            Quick Response
            Smart Learning
            Multi-channel Support
            Data Visualization
            """,
            "product_image_url": f"file://{os.path.abspath(test_image_path)}",
            "marketing_copy": """
            Revolutionary AI Customer Service Solution!
            
            - 24/7 Service
            - Smart Learning
            - Multi-channel Support
            - Complete Analytics
            """
        }
    
    def test_generate_pdf(self, pdf_generator, test_data):
        """测试PDF生成功能"""
        try:
            # 设置日志级别为 DEBUG
            logging.basicConfig(level=logging.DEBUG)
            
            # 打印图片路径信息
            print(f"\n图片路径: {test_data['product_image_url']}")
            print(f"图片文件是否存在: {os.path.exists(test_data['product_image_url'][7:])}")  # 移除 'file://' 前缀
            
            # 打印更详细的信息
            current_dir = os.getcwd()
            output_dir = os.path.join(current_dir, 'generated_pdfs')
            print("\n=== PDF生成测试信息 ===")
            print(f"当前工作目录: {current_dir}")
            print(f"目标输出目录: {output_dir}")
            print(f"输出目录是否存在: {os.path.exists(output_dir)}")
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            print(f"创建目录后是否存在: {os.path.exists(output_dir)}")
            print(f"输出目录权限: {oct(os.stat(output_dir).st_mode)[-3:]}")
            
            # 生成PDF
            print("\n正在生成PDF...")
            pdf_path = pdf_generator.generate_product_pdf(
                filename=test_data["filename"],
                product_requirements=test_data["product_requirements"],
                product_features=test_data["product_features"],
                product_image_url=test_data["product_image_url"],
                marketing_copy=test_data["marketing_copy"]
            )
            
            print(f"\nPDF生成结果:")
            print(f"PDF路径: {pdf_path}")
            print(f"文件是否存在: {os.path.exists(pdf_path)}")
            
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"文件大小: {file_size / 1024:.2f} KB")
                print(f"文件权限: {oct(os.stat(pdf_path).st_mode)[-3:]}")
            
            # 列出目录中的所有文件
            print("\n输出目录内容:")
            if os.path.exists(output_dir):
                files = os.listdir(output_dir)
                for file in files:
                    file_path = os.path.join(output_dir, file)
                    size = os.path.getsize(file_path) / 1024
                    print(f"- {file} ({size:.2f} KB)")
            else:
                print("输出目录不存在！")
            
            # 验证文件是否生成
            assert os.path.exists(pdf_path), f"PDF文件未生成: {pdf_path}"
            assert pdf_path.endswith('.pdf'), "生成的文件不是PDF格式"
            
            # 验证文件大小是否合理
            file_size = os.path.getsize(pdf_path)
            assert file_size > 0, f"PDF文件大小为0: {pdf_path}"
            
            # 存储路径供其他测试使用
            self.last_generated_pdf = pdf_path
            
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
            print(f"错误类型: {type(e)}")
            import traceback
            print(f"错误堆栈:\n{traceback.format_exc()}")
            raise

    @pytest.mark.cleanup  # 添加标记，只在指定时运行
    def test_cleanup_old_files(self, pdf_generator, test_data):
        """测试清理旧文件功能"""
        # 首先生成一个PDF
        self.test_generate_pdf(pdf_generator, test_data)
        pdf_path = self.last_generated_pdf
        
        # 测试清理功能
        pdf_generator.cleanup_old_files(max_age_hours=0)  # 立即清理
        
        # 验证文件是否被删除
        assert not os.path.exists(pdf_path)

def manual_test():
    """手动测试函数"""
    logging.basicConfig(level=logging.INFO)
    
    print("\n=== 开始手动测试 ===")
    
    # 创建测试实例
    test = TestPDFGenerator()
    pdf_generator = test.pdf_generator()
    test_data = test.test_data()
    
    try:
        # 生成PDF
        pdf_path = pdf_generator.generate_product_pdf(
            filename=test_data["filename"],
            product_requirements=test_data["product_requirements"],
            product_features=test_data["product_features"],
            product_image_url=test_data["product_image_url"],
            marketing_copy=test_data["marketing_copy"]
        )
        
        print(f"\n✅ PDF生成成功！")
        print(f"📄 文件路径: {pdf_path}")
        print(f"📊 文件大小: {os.path.getsize(pdf_path) / 1024:.2f} KB")
        
        # 打开生成的文件
        import subprocess
        try:
            subprocess.run(['start', pdf_path], shell=True)
            print(f"\n已尝试打开PDF文件，请检查是否成功打开。")
        except Exception as e:
            print(f"无法自动打开PDF文件: {e}")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        print(f"错误堆栈:\n{traceback.format_exc()}")

if __name__ == "__main__":
    manual_test() 