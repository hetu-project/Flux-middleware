from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional
from datetime import datetime
import httpx

from app.schemas.twitter import TwitterInteractionResponse
from app.services.twitter import TwitterService
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(tags=["twitter"])

@router.get("/{media_account}/interactions", response_model=TwitterInteractionResponse)
async def get_twitter_interactions(
    media_account: str,
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    username: Optional[str] = Query(None, description="用户名过滤"),
    start_time: Optional[datetime] = Query(None, description="开始时间 (ISO format with Z)"),
    end_time: Optional[datetime] = Query(None, description="结束时间 (ISO format with Z)")
) -> TwitterInteractionResponse:
    """
    获取 Twitter 互动数据
    
    Args:
        media_account: 媒体账号
        page: 页码 (>= 1)
        per_page: 每页数量 (1-100)
        username: 用户名过滤（可选）
        start_time: 开始时间（可选，格式：YYYY-MM-DDTHH:mm:ssZ）
        end_time: 结束时间（可选，格式：YYYY-MM-DDTHH:mm:ssZ）
    """
    try:
        return await TwitterService.get_interactions(
            media_account=media_account,
            page=page,
            per_page=per_page,
            username=username,
            start_time=start_time,
            end_time=end_time
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get Twitter interactions: {str(e)}"
        )

@router.post("/tweet_monitor")
@router.put("/tweet_monitor")
@router.delete("/tweet_monitor")
async def tweet_monitor(request: Request):
    """
    管理推文监控任务
    
    Methods:
        POST: 创建新的推文监控任务
        PUT: 更新现有的推文监控任务
        DELETE: 删除推文监控任务
        
    Request Body:
        media_account: str - 媒体账号
        tweet_id: str - 推文ID
        update_frequency: str - 更新频率 (可选，默认为 "10 minutes")
    """
    try:
        req = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=f"{settings.twitter_service_url}/api/subnet_tweet_task",
                json=req
            )
            return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to manage tweet monitor task: {str(e)}"
        )
