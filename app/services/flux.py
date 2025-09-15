from typing import Optional
import aiohttp
from fastapi import HTTPException

from app.core.config import get_settings
from app.schemas.flux import FluxTaskCreateRequest, FluxTaskCreateResponse

settings = get_settings()

class FluxService:
    """Flux 服务"""
    
    @staticmethod
    async def create_task(task_data: FluxTaskCreateRequest) -> FluxTaskCreateResponse:
        """
        创建 Flux 任务
        
        Args:
            task_data: 任务创建请求数据
            
        Returns:
            FluxTaskCreateResponse: Flux 任务创建响应
            
        Raises:
            HTTPException: 当请求失败时抛出
        """
        # 构建请求 URL
        url = f"{settings.FLUX_URL}/v1/task-creation/create"
        
        # 构建请求数据
        request_data = {
            "user_wallet": task_data.user_wallet,
            "project_name": task_data.project_name,
            "description": task_data.description,
            "twitter_username": task_data.twitter_username,
            "twitter_link": str(task_data.twitter_link),
            "tweet_id": task_data.tweet_id,
            "task_type": task_data.task_type.value
        }
        
        # 添加可选字段
        if task_data.project_icon:
            request_data["project_icon"] = task_data.project_icon
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=request_data) as response:
                    # 解析响应数据
                    data = await response.json()
                    
                    if response.status >= 400:
                        return FluxTaskCreateResponse(
                            success=False,
                            message=data.get("message", f"Request failed with status {response.status}")
                        )
                    
                    # 根据响应的 success 字段判断成功与否
                    if data.get("success"):
                        return FluxTaskCreateResponse(
                            success=True,
                            task_id=data.get("task_id"),
                            message=data.get("message", "Task created successfully"),
                            vlc_value=data.get("vlc_value")
                        )
                    else:
                        return FluxTaskCreateResponse(
                            success=False,
                            message=data.get("message", "Task creation failed")
                        )
                    
        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to Flux service: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
