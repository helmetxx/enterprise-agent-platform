from typing import List, Dict, Optional
import aiohttp
import asyncio
from datetime import datetime
from enum import Enum
from celery import Celery
from fastapi import BackgroundTasks, HTTPException
from redis import Redis

# 配置Celery
celery_app = Celery('knowledge_tasks', broker='redis://localhost:6379/0')

# 任务状态枚举
class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DifyKnowledgeManager:
    def __init__(self, api_key: str):
        self.api_base = "https://api.dify.ai/v1"
        self.api_key = api_key
        self.redis_client = Redis(host='localhost', port=6379, db=1)
        
    def get_task_status(self, task_id: str) -> Dict:
        """获取任务状态"""
        status = self.redis_client.hgetall(f"task:{task_id}")
        if not status:
            raise HTTPException(status_code=404, detail="Task not found")
        return status

    def update_task_status(self, task_id: str, status: Dict):
        """更新任务状态"""
        self.redis_client.hmset(f"task:{task_id}", status)
        self.redis_client.expire(f"task:{task_id}", 86400)  # 24小时过期

    async def create_knowledge_base(self, name: str, description: str) -> Dict:
        """创建知识库"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "name": name,
                "description": description,
                "indexing_technique": "high_quality"
            }
            
            async with session.post(
                f"{self.api_base}/knowledge-bases",
                headers=headers,
                json=data
            ) as response:
                return await response.json()

    async def upload_files(self, knowledge_base_id: str, files: List[str]) -> List[Dict]:
        """上传文件到知识库"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            
            results = []
            for file_path in files:
                data = aiohttp.FormData()
                data.add_field('file', 
                             open(file_path, 'rb'),
                             filename=file_path.split('/')[-1])
                
                async with session.post(
                    f"{self.api_base}/knowledge-bases/{knowledge_base_id}/files",
                    headers=headers,
                    data=data
                ) as response:
                    result = await response.json()
                    results.append(result)
                    
            return results

    async def list_knowledge_bases(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取知识库列表"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            
            params = {
                "page": page,
                "page_size": page_size
            }
            
            async with session.get(
                f"{self.api_base}/knowledge-bases",
                headers=headers,
                params=params
            ) as response:
                return await response.json()

    async def get_knowledge_base_detail(self, knowledge_base_id: str) -> Dict:
        """获取知识库详情"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            
            async with session.get(
                f"{self.api_base}/knowledge-bases/{knowledge_base_id}",
                headers=headers
            ) as response:
                return await response.json()

# Celery任务
@celery_app.task(bind=True)
def process_knowledge_base_creation(self, project_id: str, file_paths: List[str]):
    """异步处理知识库创建任务"""
    try:
        # 更新任务状态为处理中
        dify_manager = DifyKnowledgeManager(settings.DIFY_API_KEY)
        dify_manager.update_task_status(self.request.id, {
            "status": TaskStatus.PROCESSING.value,
            "progress": 0,
            "message": "Creating knowledge base..."
        })

        # 1. 创建知识库
        loop = asyncio.get_event_loop()
        kb_result = loop.run_until_complete(
            dify_manager.create_knowledge_base(
                name=f"Project_{project_id}",
                description="Project documentation knowledge base"
            )
        )
        
        knowledge_base_id = kb_result["id"]
        
        # 更新进度
        dify_manager.update_task_status(self.request.id, {
            "status": TaskStatus.PROCESSING.value,
            "progress": 30,
            "message": "Uploading files..."
        })

        # 2. 上传文件
        upload_results = loop.run_until_complete(
            dify_manager.upload_files(knowledge_base_id, file_paths)
        )

        # 3. 存储到数据库
        db.knowledge_bases.insert_one({
            "project_id": project_id,
            "knowledge_base_id": knowledge_base_id,
            "file_paths": file_paths,
            "upload_results": upload_results,
            "created_at": datetime.utcnow(),
            "task_id": self.request.id
        })

        # 更新任务完成状态
        dify_manager.update_task_status(self.request.id, {
            "status": TaskStatus.COMPLETED.value,
            "progress": 100,
            "message": "Knowledge base created successfully",
            "knowledge_base_id": knowledge_base_id
        })

        return {"status": "success", "knowledge_base_id": knowledge_base_id}

    except Exception as e:
        # 更新失败状态
        dify_manager.update_task_status(self.request.id, {
            "status": TaskStatus.FAILED.value,
            "error": str(e),
            "message": "Failed to create knowledge base"
        })
        raise

# FastAPI接口
@app.post("/api/knowledge-base/create")
async def create_knowledge_base(
    project_id: str,
    files: List[UploadFile] = File(...)
):
    """创建知识库接口 - 异步版本"""
    try:
        # 1. 保存文件到本地存储
        file_paths = []
        for file in files:
            file_path = f"uploads/{project_id}/{file.filename}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            file_paths.append(file_path)

        # 2. 创建异步任务
        task = process_knowledge_base_creation.delay(project_id, file_paths)

        # 3. 初始化任务状态
        dify_manager = DifyKnowledgeManager(settings.DIFY_API_KEY)
        dify_manager.update_task_status(task.id, {
            "status": TaskStatus.PENDING.value,
            "progress": 0,
            "message": "Task initiated",
            "project_id": project_id
        })

        return {
            "status": "accepted",
            "task_id": task.id,
            "message": "Knowledge base creation initiated"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/api/knowledge-base/status/{task_id}")
async def get_knowledge_base_status(task_id: str):
    """获取知识库创建状态"""
    try:
        dify_manager = DifyKnowledgeManager(settings.DIFY_API_KEY)
        status = dify_manager.get_task_status(task_id)
        return status
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/api/knowledge-base/list")
async def list_knowledge_bases(
    page: int = 1,
    page_size: int = 20
):
    """获取知识库列表接口"""
    try:
        dify_manager = DifyKnowledgeManager(settings.DIFY_API_KEY)
        result = await dify_manager.list_knowledge_bases(page, page_size)
        
        # 从本地数据库获取额外信息
        knowledge_bases = []
        for kb in result["data"]:
            local_info = await db.knowledge_bases.find_one(
                {"knowledge_base_id": kb["id"]}
            )
            if local_info:
                kb["local_info"] = {
                    "project_id": local_info["project_id"],
                    "created_at": local_info["created_at"],
                    "last_used": local_info.get("last_used"),
                    "usage_count": local_info.get("usage_count", 0)
                }
            knowledge_bases.append(kb)
            
        return {
            "status": "success",
            "data": knowledge_bases,
            "total": result["total"],
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/api/knowledge-base/select")
async def select_knowledge_base(
    project_id: str,
    knowledge_base_id: str
):
    """选择使用现有知识库"""
    try:
        dify_manager = DifyKnowledgeManager(settings.DIFY_API_KEY)
        
        # 1. 验证知识库是否存在
        kb_detail = await dify_manager.get_knowledge_base_detail(knowledge_base_id)
        
        # 2. 更新或创建本地记录
        await db.knowledge_bases.update_one(
            {"knowledge_base_id": knowledge_base_id},
            {
                "$set": {
                    "project_id": project_id,
                    "last_used": datetime.utcnow()
                },
                "$inc": {
                    "usage_count": 1
                }
            },
            upsert=True
        )
        
        return {
            "status": "success",
            "message": "Knowledge base selected successfully",
            "knowledge_base_id": knowledge_base_id
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        } 