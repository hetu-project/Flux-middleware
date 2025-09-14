from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class Interaction(BaseModel):
    """Twitter 互动数据模型"""
    interaction_id: str
    user_id: str
    username: str
    avatar_url: HttpUrl
    interaction_type: str
    interaction_content: str
    interaction_time: datetime
    post_id: str
    post_time: datetime

class PaginationInfo(BaseModel):
    """分页信息"""
    current_page: int
    per_page: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool

class TwitterInteractionResponse(BaseModel):
    """Twitter 互动数据响应"""
    media_account: str
    username: Optional[str] = None
    pagination: PaginationInfo
    interactions: List[Interaction]

class SubnetTweetTaskRequest(BaseModel):
    """子网推文任务请求"""
    media_account: str
    tweet_id: str
    update_frequency: Optional[str] = "6 hours"

class SubnetTweetTaskResponse(BaseModel):
    """子网推文任务响应"""
    success: bool
    message: str

class RetweetCheckRequest(BaseModel):
    """Retweet检测请求"""
    media_account: str = Field(..., description="媒体账号")
    x_id: str = Field(..., description="用户ID")
    post_id: str = Field(..., description="帖子ID")
    start_time: datetime = Field(..., description="开始时间 (ISO format with Z)")
    end_time: datetime = Field(..., description="结束时间 (ISO format with Z)")

class RetweetCheckResponse(BaseModel):
    """Retweet检测响应"""
    has_retweet: bool = Field(..., description="是否有retweet操作")
    message: str = Field(..., description="响应消息")
