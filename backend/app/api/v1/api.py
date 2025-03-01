from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, creative, agents, knowledge

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(creative.router, prefix="/creative", tags=["creative"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])

@api_router.get("/test")
async def test():
    return {"message": "API is working!"}

# 后续会添加更多路由 