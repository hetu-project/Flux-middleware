from pydantic import BaseModel, HttpUrl
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
