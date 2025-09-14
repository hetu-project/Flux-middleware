from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional
from datetime import datetime
import httpx

from app.schemas.twitter import TwitterInteractionResponse, SubnetTweetTaskRequest, SubnetTweetTaskResponse, RetweetCheckRequest, RetweetCheckResponse
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
    x_id: Optional[str] = Query(None, description="用户ID过滤"),
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
        x_id: 用户ID过滤（可选）
        start_time: 开始时间（可选，格式：YYYY-MM-DDTHH:mm:ssZ）
        end_time: 结束时间（可选，格式：YYYY-MM-DDTHH:mm:ssZ）
    """
    try:
        return await TwitterService.get_interactions(
            media_account=media_account,
            page=page,
            per_page=per_page,
            username=username,
            x_id=x_id,
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

@router.post("/subnet_tweet_task", response_model=SubnetTweetTaskResponse)
@router.put("/subnet_tweet_task", response_model=SubnetTweetTaskResponse)
@router.delete("/subnet_tweet_task", response_model=SubnetTweetTaskResponse)
async def subnet_tweet_task(
    request: Request,
    task_data: SubnetTweetTaskRequest
) -> SubnetTweetTaskResponse:
    """
    处理子网推文任务
    
    Methods:
        POST: 创建新的子网推文任务
        PUT: 更新现有的子网推文任务
        DELETE: 删除子网推文任务
        
    Request Body:
        media_account: str - 媒体账号
        tweet_id: str - 推文ID
        update_frequency: str - 更新频率 (可选，默认为 "10 minutes")
    """
    try:
        return await TwitterService.subnet_tweet_task(
            method=request.method,
            task_data=task_data
        )
    except Exception as e:
        return SubnetTweetTaskResponse(
            success=False,
            message=f"Failed to process subnet tweet task: {str(e)}"
        )

@router.post("/retweet-check", response_model=RetweetCheckResponse)
async def check_user_retweet(
    request: RetweetCheckRequest
) -> RetweetCheckResponse:
    """
    检测用户在指定时间段内是否有对特定帖子的retweet操作
    
    Args:
        request: Retweet检测请求数据
        
    Returns:
        RetweetCheckResponse: 检测结果响应
    """
    try:
        has_retweet = await TwitterService.check_user_retweet(
            media_account=request.media_account,
            x_id=request.x_id,
            post_id=request.post_id,
            start_time=request.start_time,
            end_time=request.end_time
        )
        
        return RetweetCheckResponse(
            has_retweet=has_retweet,
            message=f"User {request.x_id} {'has' if has_retweet else 'has not'} retweeted post {request.post_id} in the specified time range"
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check user retweet: {str(e)}"
        )
