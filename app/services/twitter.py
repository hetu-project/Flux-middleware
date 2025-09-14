from typing import Optional
from datetime import datetime
import aiohttp
from fastapi import HTTPException

from app.core.config import get_settings
from app.schemas.twitter import TwitterInteractionResponse, SubnetTweetTaskRequest, SubnetTweetTaskResponse

settings = get_settings()

class TwitterService:
    """Twitter 服务"""
    
    @staticmethod
    async def get_interactions(
        media_account: str,
        page: int = 1,
        per_page: int = 10,
        username: Optional[str] = None,
        x_id: Optional[str] = None,
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
            x_id: 用户ID过滤
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            TwitterInteractionResponse: Twitter 互动数据响应
            
        Raises:
            HTTPException: 当请求失败时抛出
        """
        # 构建请求 URL
        url = f"{settings.twitter_service_url}/api/interaction/{media_account}"
        
        # 验证分页参数
        if page < 1:
            raise HTTPException(
                status_code=400,
                detail="Page number must be greater than 0"
            )
        if per_page < 1 or per_page > 100:
            raise HTTPException(
                status_code=400,
                detail="Items per page must be between 1 and 100"
            )
        
        # 构建查询参数
        params = {
            "page": str(page),  # aiohttp 需要字符串类型的参数
            "per_page": str(per_page)
        }
        
        if username:
            params["username"] = username
            
        if x_id:
            params["x_id"] = x_id
            
        if start_time:
            # 验证时间格式并转换为原生后端期望的格式
            try:
                # 移除时区信息，只保留 YYYY-MM-DDTHH:mm:ssZ 格式
                start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                params["start_time"] = start_time_str
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid start time format, require YYYY-MM-DDTHH:mm:ssZ format"
                )
            
        if end_time:
            # 验证时间格式并转换为原生后端期望的格式
            try:
                # 移除时区信息，只保留 YYYY-MM-DDTHH:mm:ssZ 格式
                end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                params["end_time"] = end_time_str
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid end time format, require YYYY-MM-DDTHH:mm:ssZ format"
                )
            
        try:
            # 添加调试信息
            print(f"Request URL: {url}")
            print(f"Request params: {params}")
            
            # 使用 aiohttp.ClientSession 的上下文管理器
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    print(f"Response status: {response.status}")
                    
                    if response.status >= 400:
                        # 尝试获取错误响应内容
                        try:
                            error_data = await response.json()
                            error_message = error_data.get("message", f"Twitter service returned error: {response.status}")
                        except:
                            error_message = f"Twitter service returned error: {response.status}"
                        
                        print(f"Error response: {error_message}")
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Twitter service error: {error_message}"
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
    
    @staticmethod
    async def subnet_tweet_task(
        method: str,
        task_data: SubnetTweetTaskRequest
    ) -> SubnetTweetTaskResponse:
        """
        处理子网推文任务（创建、更新、删除）
        
        Args:
            method: HTTP 方法 (POST, PUT, DELETE)
            task_data: 任务数据
            
        Returns:
            SubnetTweetTaskResponse: 任务操作响应
            
        Raises:
            HTTPException: 当请求失败时抛出
        """
        # 构建请求 URL
        url = f"{settings.twitter_service_url}/api/subnet_tweet_task"
        
        # 构建请求数据
        request_data = {
            "media_account": task_data.media_account,
            "tweet_id": task_data.tweet_id
        }
        
        if method in ["POST", "PUT"]:
            request_data["update_frequency"] = task_data.update_frequency
        
        try:
            async with aiohttp.ClientSession() as session:
                if method == "DELETE":
                    async with session.delete(url, json=request_data) as response:
                        data = await response.json()
                else:
                    async with session.post(url, json=request_data) as response:
                        data = await response.json()
                
                if response.status >= 400:
                    return SubnetTweetTaskResponse(
                        success=False,
                        message=data.get("message", f"Request failed with status {response.status}")
                    )
                
                # 根据原始响应的 status 字段判断成功与否
                if data.get("status") == "success":
                    return SubnetTweetTaskResponse(
                        success=True,
                        message=data.get("message", "Operation completed successfully")
                    )
                else:
                    return SubnetTweetTaskResponse(
                        success=False,
                        message=data.get("message", "Operation failed")
                    )
                    
        except aiohttp.ClientError as e:
            return SubnetTweetTaskResponse(
                success=False,
                message=f"Failed to connect to Twitter service: {str(e)}"
            )
        except Exception as e:
            return SubnetTweetTaskResponse(
                success=False,
                message=f"Internal server error: {str(e)}"
            )
    
    @staticmethod
    async def check_user_retweet(
        media_account: str,
        x_id: str,
        post_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """
        检测用户在指定时间段内是否有对特定帖子的retweet操作
        
        Args:
            media_account: 媒体账号
            x_id: 用户ID
            post_id: 帖子ID
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            bool: 如果用户在指定时间段内对指定帖子进行了retweet操作则返回True，否则返回False
            
        Raises:
            HTTPException: 当请求失败时抛出
        """
        page = 1
        per_page = 100  # 每页获取更多数据以提高效率
        
        try:
            while True:
                # 调用现有的get_interactions服务获取数据
                response = await TwitterService.get_interactions(
                    media_account=media_account,
                    page=page,
                    per_page=per_page,
                    x_id=x_id,
                    start_time=start_time,
                    end_time=end_time
                )
                
                # 检查当前页的interactions中是否有匹配的retweet操作
                for interaction in response.interactions:
                    # 检查是否是retweet操作且post_id匹配
                    if (interaction.interaction_type.lower() == "retweet" and 
                        interaction.post_id == post_id):
                        return True
                
                # 如果没有找到retweet操作，检查是否还有下一页
                if not response.pagination.has_next:
                    break
                    
                page += 1
                
            # 遍历完所有页面都没有找到retweet操作
            return False
            
        except HTTPException as e:
            # 如果是HTTP异常，重新抛出
            raise e
        except Exception as e:
            # 其他异常，抛出HTTP异常
            raise HTTPException(
                status_code=500,
                detail=f"Failed to check user retweet: {str(e)}"
            )
