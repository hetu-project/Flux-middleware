from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime

from app.schemas.twitter import TwitterInteractionResponse
from app.services.twitter import TwitterService

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
