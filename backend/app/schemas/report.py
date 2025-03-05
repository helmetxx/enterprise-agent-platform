from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from enum import Enum


class ReportFormat(str, Enum):
    """报表格式枚举"""
    PDF = "PDF"
    EXCEL = "EXCEL"
    WORD = "WORD"


class ReportRequest(BaseModel):
    """报表请求模型"""
    identity: str = Field(..., description="报表标识符，如 MRCWBG")
    format_type: ReportFormat = Field(..., description="输出格式")
    parameters: Dict[str, Any] = Field(..., description="报表参数")
    app_code: Optional[str] = Field("INN", description="应用代码")

    class Config:
        # 添加示例，帮助API文档和测试
        schema_extra = {
            "example": {
                "identity": "MRCWBG",
                "format_type": "PDF",
                "parameters": {"bizDate": "2025-03-02"},
                "app_code": "INN"
            }
        }


class ReportResponse(BaseModel):
    """报表响应模型（用于API文档）"""
    filename: str = Field(..., description="文件名")
    content_type: str = Field(..., description="内容类型")
    # 注意：实际响应是文件流，不是JSON 


class ReportStatusResponse(BaseModel):
    report_id: str
    status: str


# 添加新的 schema 用于报表导出
class ReportExportRequest(BaseModel):
    identity: str
    format_type: str
    parameters: Dict[str, Any]
    app_code: str = "INN" 