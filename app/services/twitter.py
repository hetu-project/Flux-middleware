from typing import Optional
from datetime import datetime
import aiohttp
from fastapi import HTTPException

from app.core.config import get_settings
from app.schemas.twitter import TwitterInteractionResponse

settings = get_settings()

class TwitterService:
    """Twitter 服务"""
    
    @staticmethod
    async def get_interactions(
        media_account: str,
        page: int = 1,
        per_page: int = 10,
        username: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> TwitterInteractionResponse:
        """
        获取 Twitter 互动数据
        
        Args:
            media_account: 媒体账号
            page: 页码
            per_page: 每页数量
            username: 用户名过滤
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            TwitterInteractionResponse: Twitter 互动数据响应
            
        Raises:
            HTTPException: 当请求失败时抛出
        """
        # 构建请求 URL
        url = f"{settings.twitter_service_url}/api/interaction/{media_account}"
        
        # 构建查询参数
        params = {
            "page": str(page),  # aiohttp 需要字符串类型的参数
            "per_page": str(per_page)
        }
        
        if username:
            params["username"] = username
            
        if start_time:
            params["start_time"] = start_time.isoformat() + "Z"
            
        if end_time:
            params["end_time"] = end_time.isoformat() + "Z"
            
        try:
            # 使用 aiohttp.ClientSession 的上下文管理器
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status >= 400:
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Twitter service returned error: {response.status}"
                        )
                    
                    # 解析响应数据
                    data = await response.json()
                    return TwitterInteractionResponse(**data)
                    
        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch Twitter interactions: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
