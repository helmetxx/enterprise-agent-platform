from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import requests
from io import BytesIO
from PIL import Image as PILImage
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self):
        # 注册中文字体
        try:
            font_path = os.path.join(os.path.dirname(__file__), '../static/fonts/SimHei.ttf')
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('SimHei', font_path))
            else:
                # 使用系统默认字体作为后备
                pdfmetrics.registerFont(TTFont('SimHei', 'arial.ttf'))
        except Exception as e:
            logger.warning(f"Failed to register SimHei font: {e}")
            # 如果字体注册失败，使用默认字体
            self.use_default_font = True
        
        # 创建自定义样式
        self.styles = getSampleStyleSheet()
        font_name = 'SimHei' if not getattr(self, 'use_default_font', False) else 'Helvetica'
        
        self.styles.add(ParagraphStyle(
            name='ChineseTitle',
            fontName=font_name,
            fontSize=24,
            spaceAfter=30,
            alignment=1
        ))
        self.styles.add(ParagraphStyle(
            name='ChineseHeading',
            fontName='SimHei',
            fontSize=16,
            spaceAfter=12,
            spaceBefore=24
        ))
        self.styles.add(ParagraphStyle(
            name='ChineseBody',
            fontName='SimHei',
            fontSize=12,
            spaceAfter=8,
            leading=20
        ))

    def _download_image(self, image_url: str) -> Image:
        """下载并处理图片"""
        try:
            logger.info(f"Attempting to download image from: {image_url}")
            
            if image_url.startswith('file://'):
                # 处理本地文件
                local_path = image_url[7:]  # 移除 'file://' 前缀
                logger.info(f"Loading local image from: {local_path}")
                # 使用 PIL 打开并转换图片
                with PILImage.open(local_path) as img:
                    # 转换为 RGB 模式（如果是 RGBA，移除透明通道）
                    if img.mode in ('RGBA', 'LA'):
                        background = PILImage.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 保存为临时文件
                    temp_buffer = BytesIO()
                    img.save(temp_buffer, format='JPEG')
                    temp_buffer.seek(0)
                    
                    # 创建 ReportLab Image 对象
                    img = Image(temp_buffer)
            else:
                # 处理远程图片
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(image_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # 使用 PIL 处理图片
                with PILImage.open(BytesIO(response.content)) as img:
                    # 转换为 RGB 模式
                    if img.mode in ('RGBA', 'LA'):
                        background = PILImage.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # 保存为临时文件
                    temp_buffer = BytesIO()
                    img.save(temp_buffer, format='JPEG')
                    temp_buffer.seek(0)
                    
                    # 创建 ReportLab Image 对象
                    img = Image(temp_buffer)
            
            # 调整图片大小
            max_width = A4[0] * 0.8  # A4纸宽度的80%
            if img.drawWidth > max_width:
                ratio = max_width / img.drawWidth
                img.drawWidth = max_width
                img.drawHeight *= ratio
            
            # 设置图片居中
            img.hAlign = 'CENTER'
            
            logger.info(f"Successfully processed image. Size: {img.drawWidth}x{img.drawHeight}")
            return img
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}", exc_info=True)
            raise

    def generate_product_pdf(self, filename: str, product_requirements: str, 
                            product_features: str, product_image_url: str, 
                            marketing_copy: str) -> str:
        """生成产品PDF文件
        
        Args:
            filename: 文件名
            product_requirements: 产品需求
            product_features: 产品特点
            product_image_url: 产品图片URL
            marketing_copy: 营销文案
            
        Returns:
            str: 生成的PDF文件路径
        """
        # 创建输出目录
        output_dir = os.path.join(os.getcwd(), 'generated_pdfs')
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(output_dir, f'{filename}_{timestamp}.pdf')
        
        # 创建PDF文档
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # 创建内容列表
        story = []
        
        # 添加标题
        story.append(Paragraph(filename, self.styles['ChineseTitle']))
        story.append(Spacer(1, 20))
        
        # 添加产品图片
        try:
            img = self._download_image(product_image_url)
            # 添加图片标题
            story.append(Paragraph('Product Image', self.styles['ChineseHeading']))
            story.append(img)
            story.append(Spacer(1, 20))
        except Exception as e:
            logger.warning(f"Failed to add image: {e}")
            # 添加图片错误提示
            story.append(Paragraph('(Image loading failed)', 
                                 ParagraphStyle('Error', 
                                              parent=self.styles['ChineseBody'],
                                              textColor=colors.red)))
            story.append(Spacer(1, 20))
        
        # 添加产品需求
        story.append(Paragraph('Product Requirements', self.styles['ChineseHeading']))
        story.append(Paragraph(product_requirements, self.styles['ChineseBody']))
        story.append(Spacer(1, 20))
        
        # 添加产品特点
        story.append(Paragraph('Product Features', self.styles['ChineseHeading']))
        # 将特点拆分为列表
        features = product_features.strip().split('\n')
        for feature in features:
            if feature.strip():
                story.append(Paragraph(f"• {feature.strip()}", self.styles['ChineseBody']))
        story.append(Spacer(1, 20))
        
        # 添加营销文案
        story.append(Paragraph('Marketing Copy', self.styles['ChineseHeading']))
        story.append(Paragraph(marketing_copy, self.styles['ChineseBody']))
        
        # 生成PDF
        try:
            doc.build(story)
            logger.info(f"Successfully generated PDF: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise

    def cleanup_old_files(self, max_age_hours: int = 24):
        """清理旧的PDF文件"""
        output_dir = os.path.join(os.getcwd(), 'generated_pdfs')
        if not os.path.exists(output_dir):
            return
            
        current_time = datetime.now()
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            file_age = current_time - datetime.fromtimestamp(os.path.getctime(file_path))
            
            if file_age.total_seconds() > (max_age_hours * 3600):
                try:
                    os.remove(file_path)
                    logger.info(f"Removed old PDF file: {file_path}")
                except Exception as e:
                    logger.error(f"Error removing old PDF file {file_path}: {str(e)}") 