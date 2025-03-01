from fastapi.openapi.utils import get_openapi
from app.main import app

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Enterprise Agent Platform API",
        version="1.0.0",
        description="API documentation for Enterprise Agent Platform",
        routes=app.routes,
    )
    
    # 自定义安全方案
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # 为所有路由添加安全要求
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    # 添加标签描述
    openapi_schema["tags"] = [
        {
            "name": "auth",
            "description": "Authentication operations"
        },
        {
            "name": "agents",
            "description": "Agent management operations"
        },
        {
            "name": "chat",
            "description": "Chat operations"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi 