import os
import tempfile
import logging
import datetime
import shutil
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, Response, JSONResponse
from typing import Any, List, Dict

from app.schemas.report import ReportRequest, ReportResponse, ReportFormat
from app.services.report_service import ReportService
from app.core.config import settings
from app.api import deps
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

# 确保临时目录存在
os.makedirs(settings.REPORT_TEMP_DIR, exist_ok=True)
logger.info(f"Ensuring report temp directory exists: {settings.REPORT_TEMP_DIR}")

# 确保报表存储目录存在
os.makedirs(settings.REPORT_STORAGE_DIR, exist_ok=True)
logger.info(f"Ensuring report storage directory exists: {settings.REPORT_STORAGE_DIR}")


def generate_report_filename(identity: str, format_type: str) -> str:
    """
    生成唯一的报表文件名
    
    格式: {identity}_REPORT_{timestamp}.{extension}
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_extension = format_type.lower()
    if file_extension == "excel":
        file_extension = "xlsx"
    elif file_extension == "word":
        file_extension = "docx"
    
    return f"{identity}_REPORT_{timestamp}.{file_extension}"


@router.post("/export", response_model=Dict[str, Any])
async def export_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    导出报表
    
    从外部系统导出报表，保存到服务器，并返回文件URL
    """
    try:
        # 生成唯一的文件名
        filename = generate_report_filename(request.identity, request.format_type.value)
        
        # 创建临时文件
        file_extension = request.format_type.value.lower()
        if file_extension == "excel":
            file_extension = "xlsx"
        elif file_extension == "word":
            file_extension = "docx"
            
        fd, temp_path = tempfile.mkstemp(suffix=f".{file_extension}", dir=settings.REPORT_TEMP_DIR)
        os.close(fd)
        
        logger.info(f"Exporting report {request.identity} in {request.format_type} format")
        logger.info(f"Temporary file path: {temp_path}")
        
        # 导出报表
        ReportService.export_report(
            identity=request.identity,
            format_type=request.format_type.value,
            parameters=request.parameters,
            app_code=request.app_code,
            save_path=temp_path
        )
        
        # 确定最终存储路径
        storage_path = os.path.join(settings.REPORT_STORAGE_DIR, filename)
        
        # 将临时文件移动到存储目录
        shutil.move(temp_path, storage_path)
        logger.info(f"Moved report to storage location: {storage_path}")
        
        # 生成完整的访问URL，包含主机名和端口
        report_url = f"{settings.SERVER_HOST}{settings.REPORT_URL_BASE}/{filename}"
        
        # 设置内容类型
        content_type_map = {
            ReportFormat.PDF: "application/pdf",
            ReportFormat.EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ReportFormat.WORD: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        content_type = content_type_map.get(request.format_type, "application/octet-stream")
        
        # 返回优化后的JSON响应
        return {
            "status": "success",
            "message": "报表生成成功",
            "url": report_url,
            "report_id": filename.split('.')[0],
            "filename": filename,
            "content_type": content_type,
            "format": request.format_type.value,
            "created_at": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.exception(f"Error exporting report: {str(e)}")
        return {
            "status": "error",
            "message": f"导出报表失败: {str(e)}",
            "url": None,
            "report_id": None,
            "filename": None,
            "content_type": None,
            "format": None,
            "created_at": datetime.datetime.now().isoformat()
        }


@router.post("/simple_export", response_model=Dict[str, Any])
async def simple_export_report(
    identity: str = "MRCWBG",
    format_type: str = "PDF",
    biz_date: str = "2025-03-02",
    app_code: str = "INN",
) -> Any:
    """
    简化版报表导出接口，用于测试
    
    使用查询参数而不是JSON请求体
    
    参数:
    - identity: 报表标识符，如 MRCWBG
    - format_type: 输出格式，如 PDF, EXCEL, WORD
    - biz_date: 业务日期，如 2025-03-02
    - app_code: 应用代码，默认为 INN
    
    返回:
    - JSON对象，包含报表文件的URL
    """
    try:
        # 生成唯一的文件名
        filename = generate_report_filename(identity, format_type)
        
        # 创建临时文件
        file_extension = format_type.lower()
        if file_extension == "excel":
            file_extension = "xlsx"
        elif file_extension == "word":
            file_extension = "docx"
            
        fd, temp_path = tempfile.mkstemp(suffix=f".{file_extension}", dir=settings.REPORT_TEMP_DIR)
        os.close(fd)
        
        logger.info(f"[Simple Export] Exporting report {identity} in {format_type} format")
        logger.info(f"[Simple Export] Temporary file path: {temp_path}")
        
        # 导出报表
        ReportService.export_report(
            identity=identity,
            format_type=format_type,
            parameters={"bizDate": biz_date},
            app_code=app_code,
            save_path=temp_path
        )
        
        # 确定最终存储路径
        storage_path = os.path.join(settings.REPORT_STORAGE_DIR, filename)
        
        # 将临时文件移动到存储目录
        shutil.move(temp_path, storage_path)
        logger.info(f"[Simple Export] Moved report to storage location: {storage_path}")
        
        # 生成完整的访问URL，包含主机名和端口
        report_url = f"{settings.SERVER_HOST}{settings.REPORT_URL_BASE}/{filename}"
        
        # 设置内容类型
        content_type = "application/pdf"
        if format_type.upper() == "EXCEL":
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format_type.upper() == "WORD":
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        # 返回优化后的JSON响应
        return {
            "status": "success",
            "message": "报表生成成功",
            "url": report_url,
            "report_id": filename.split('.')[0],
            "filename": filename,
            "content_type": content_type,
            "format": format_type,
            "created_at": datetime.datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.exception(f"[Simple Export] Error exporting report: {str(e)}")
        return {
            "status": "error",
            "message": f"导出报表失败: {str(e)}",
            "url": None,
            "report_id": None,
            "filename": None,
            "content_type": None,
            "format": None,
            "created_at": datetime.datetime.now().isoformat()
        }


@router.get("/test")
async def test_reports_api():
    """
    测试报表 API 是否正常工作
    """
    return {"status": "ok", "message": "Reports API is working"}

# 添加一个新的端点，用于在 Swagger UI 中查看报表导出的详细信息
@router.post("/export_info", response_model=dict)
async def export_report_info(
    request: ReportRequest,
) -> Any:
    """
    获取报表导出信息（用于调试）
    
    返回报表导出的详细信息，而不是实际下载文件
    """
    try:
        # 创建临时文件路径（但不实际创建文件）
        file_extension = request.format_type.value.lower()
        if file_extension == "excel":
            file_extension = "xlsx"
        elif file_extension == "word":
            file_extension = "docx"
            
        temp_path = f"{settings.REPORT_TEMP_DIR}/report_{request.identity}_{file_extension}"
        
        # 设置内容类型
        content_type_map = {
            ReportFormat.PDF: "application/pdf",
            ReportFormat.EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ReportFormat.WORD: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        content_type = content_type_map.get(request.format_type, "application/octet-stream")
        
        # 生成文件名
        filename = f"report_{request.identity}.{file_extension}"
        
        # 返回信息
        return {
            "request": {
                "identity": request.identity,
                "format_type": request.format_type.value,
                "parameters": request.parameters,
                "app_code": request.app_code
            },
            "response": {
                "filename": filename,
                "content_type": content_type,
                "temp_path": temp_path
            },
            "note": "这是一个调试端点，不会实际生成报表文件。请使用 /api/reports/export 或 /api/reports/simple_export 端点下载实际的报表文件。"
        }
        
    except Exception as e:
        logger.exception(f"Error getting report export info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取报表导出信息失败: {str(e)}") 