import httpx
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)

class DifyClient:
    def __init__(self):
        self.base_url = settings.DIFY_API_BASE_URL
        self.api_key = settings.DIFY_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_knowledge_base(self, name: str, description: str = None) -> dict:
        """创建 DIFY 知识库"""
        url = f"{self.base_url}/datasets"
        data = {
            "name": name,
            "description": description or "",
            "permission": "only_me"
        }
        
        logger.info(f"Creating DIFY knowledge base at URL: {url}")
        logger.info(f"Request data: {json.dumps(data)}")
        logger.info(f"Headers: {json.dumps(self.headers)}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=data
                )
                
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response body: {response.text}")
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {str(e)}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {str(e)}")
            logger.error(f"Response: {getattr(e.response, 'text', 'No response text')}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    async def create_document_by_file(
        self, 
        dataset_id: str, 
        file_path: str,
        file_name: str
    ) -> dict:
        """通过文件创建文档"""
        url = f"{self.base_url}/datasets/{dataset_id}/document/create-by-file"
        
        # 准备处理规则JSON
        data = {
            "indexing_technique": "high_quality",
            "process_rule": {
                "rules": {
                    "pre_processing_rules": [
                        {"id": "remove_extra_spaces", "enabled": True},
                        {"id": "remove_urls_emails", "enabled": True}
                    ],
                    "segmentation": {
                        "separator": "###",
                        "max_tokens": 500
                    }
                },
                "mode": "custom"
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                with open(file_path, 'rb') as f:
                    # 注意这里的变化：data参数需要是JSON字符串
                    files = {
                        'file': (file_name, f, 'text/plain'),
                        'data': ('', json.dumps(data), 'application/json')
                    }
                    
                    response = await client.post(
                        url,
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        files=files
                    )
                    
                    logger.info(f"Create document response: {response.text}")
                    response.raise_for_status()
                    return response.json()

        except Exception as e:
            logger.error(f"Error creating document in DIFY: {str(e)}")
            raise

dify_client = DifyClient() 