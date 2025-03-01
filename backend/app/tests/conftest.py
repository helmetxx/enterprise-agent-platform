import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 创建必要的目录
def setup_test_environment():
    # 创建字体目录
    fonts_dir = project_root / "app" / "static" / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建PDF输出目录
    pdf_dir = project_root / "generated_pdfs"
    pdf_dir.mkdir(exist_ok=True)
    
    # 确保字体文件存在
    font_file = fonts_dir / "SimHei.ttf"
    if not font_file.exists():
        # 如果字体文件不存在，可以从系统字体目录复制，或者提供一个默认字体
        # 这里使用 Arial 作为后备字体
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase import pdfmetrics
        pdfmetrics.registerFont(TTFont('SimHei', 'arial.ttf'))

setup_test_environment() 