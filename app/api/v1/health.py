from fastapi import APIRouter
from typing import Dict

router = APIRouter(tags=["health"])

@router.get("/ping", response_model=Dict[str, str])
async def ping() -> Dict[str, str]:
    """
    健康检查接口
    
    Returns:
        Dict[str, str]: 包含 "message" 字段的响应
    """
    return {"message": "pong"}
