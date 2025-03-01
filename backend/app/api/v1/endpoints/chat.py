from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict
from app import crud, schemas
from app.api import deps
from app.core.websocket import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    db = Depends(deps.get_db)
):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            # 处理消息
            message = schemas.ChatMessage(
                content=data["content"],
                session_id=data["sessionId"],
                sender="user"
            )
            # 保存消息到数据库
            crud.message.create(db, obj_in=message)
            # 发送消息给AI处理
            response = await process_message(data["content"])
            # 广播AI响应
            await manager.broadcast(response, client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id) 