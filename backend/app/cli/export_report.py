#!/usr/bin/env python
"""
报表导出命令行工具

使用方法:
    python -m app.cli.export_report --identity MRCWBG --format PDF --param bizDate=2025-03-02 --output report.pdf
"""

import argparse
import json
import sys
import os
import logging
import traceback
from app.services.report_service import ReportService
from app.core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_params(param_list):
    """解析参数列表为字典"""
    params = {}
    for param in param_list:
        if '=' in param:
            key, value = param.split('=', 1)
            params[key] = value
        else:
            logger.warning(f"忽略无效参数: {param}")
    return params

def main():
    parser = argparse.ArgumentParser(description='从外部系统导出报表')
    parser.add_argument('--identity', required=True, help='报表标识符，如 MRCWBG')
    parser.add_argument('--format', required=True, choices=['PDF', 'EXCEL', 'WORD'], help='输出格式')
    parser.add_argument('--param', action='append', default=[], help='报表参数，格式为 key=value')
    parser.add_argument('--app-code', default='INN', help='应用代码，默认为 INN')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    # 如果启用调试模式，设置日志级别为 DEBUG
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 解析参数
    parameters = parse_params(args.param)
    
    logger.info(f"导出报表: {args.identity}, 格式: {args.format}")
    logger.info(f"参数: {parameters}")
    logger.info(f"输出文件: {args.output}")
    logger.info(f"报表 API URL: {settings.REPORT_API_BASE_URL}{settings.REPORT_API_PATH}")
    
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"创建输出目录: {output_dir}")
        
        # 导出报表
        logger.info("开始导出报表...")
        content = ReportService.export_report(
            identity=args.identity,
            format_type=args.format,
            parameters=parameters,
            app_code=args.app_code,
            save_path=args.output
        )
        
        logger.info(f"报表导出成功，大小: {len(content)} 字节")
        logger.info(f"已保存到: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"报表导出失败: {e}")
        if args.debug:
            logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main()) 