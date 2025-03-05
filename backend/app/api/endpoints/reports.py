import os
import tempfile
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, Response
from typing import Any, List

from app.schemas.report import ReportRequest, ReportResponse, ReportFormat, ReportExportRequest
from app.services.report_service import ReportService
from app.core.config import settings
from app.api import deps
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

# 确保临时目录存在
os.makedirs(settings.REPORT_TEMP_DIR, exist_ok=True)
logger.info(f"Ensuring report temp directory exists: {settings.REPORT_TEMP_DIR}")


@router.post("/export", response_model=None, responses={
    200: {
        "content": {
            "application/pdf": {},
            "application/vnd.ms-excel": {},
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {},
        },
        "description": "返回报表文件",
    }
})
async def export_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    导出报表
    
    从外部系统导出报表并返回文件
    """
    try:
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
        
        # 设置清理任务
        background_tasks.add_task(os.unlink, temp_path)
        
        # 设置内容类型
        content_type_map = {
            ReportFormat.PDF: "application/pdf",
            ReportFormat.EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ReportFormat.WORD: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        content_type = content_type_map.get(request.format_type, "application/octet-stream")
        
        # 生成文件名
        filename = f"report_{request.identity}.{file_extension}"
        
        logger.info(f"Returning report file: {filename}")
        
        # 返回文件
        return FileResponse(
            path=temp_path,
            filename=filename,
            media_type=content_type,
            background=background_tasks
        )
        
    except Exception as e:
        logger.exception(f"Error exporting report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导出报表失败: {str(e)}")

@router.get("/test")
async def test_reports_api():
    """
    测试报表 API 是否正常工作
    """
    return {"status": "ok", "message": "Reports API is working"} 