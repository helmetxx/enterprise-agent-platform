import requests
import logging
from typing import Dict, Optional, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class ReportService:
    """
    服务类，用于与外部报表系统交互
    """
    
    @staticmethod
    def export_report(
        identity: str,
        format_type: str,
        parameters: Dict[str, Any],
        app_code: str = "INN",
        save_path: Optional[str] = None
    ) -> bytes:
        """
        从外部系统导出报表
        
        Args:
            identity: 报表标识符，如 "MRCWBG"
            format_type: 输出格式，如 "PDF", "EXCEL"
            parameters: 报表参数，如 {"bizDate": "2025-03-02"}
            app_code: 应用代码，默认为 "INN"
            save_path: 可选，如果提供则保存文件到指定路径
            
        Returns:
            bytes: 报表文件的二进制内容
            
        Raises:
            HTTPError: 当 API 请求失败时
            IOError: 当文件保存失败时
        """
        url = f"{settings.REPORT_API_BASE_URL}{settings.REPORT_API_PATH}"
        
        headers = {
            "Authorization": settings.REPORT_API_AUTH_TOKEN,
            "Content-Type": "application/json;charset=UTF-8",
            "language": settings.REPORT_API_LANGUAGE
        }
        
        payload = {
            "appCode": app_code,
            "identity": identity,
            "format": format_type,
            "parameters": parameters
        }
        
        logger.info(f"Calling external report API: {url}")
        logger.debug(f"Report request payload: {payload}")
        
        try:
            # 发送请求
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            # 检查响应状态
            response.raise_for_status()
            
            # 获取二进制内容
            content = response.content
            
            logger.info(f"Report generated successfully, size: {len(content)} bytes")
            
            # 如果提供了保存路径，则保存文件
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(content)
                logger.info(f"Report saved to {save_path}")
            
            return content
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error when calling report API: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error when calling report API: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout when calling report API: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling report API: {e}")
            raise
        except IOError as e:
            logger.error(f"IO error when saving report: {e}")
            raise 