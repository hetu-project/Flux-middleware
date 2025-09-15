from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from app.schemas.enums import TaskType
class FluxTaskCreateRequest(BaseModel):
    """Flux 任务创建请求"""
    user_wallet: str = Field(..., description="用户钱包地址")
    project_name: str = Field(..., description="项目名称")
    project_icon: Optional[str] = Field(None, description="项目图标URL")
    description: str = Field(..., description="项目描述")
    twitter_username: str = Field(..., description="Twitter用户名")
    twitter_link: HttpUrl = Field(..., description="Twitter链接")
    tweet_id: str = Field(..., description="推文ID")
    task_type: TaskType = Field(..., description="任务类型")

class FluxTaskCreateResponse(BaseModel):
    """Flux 任务创建响应"""
    success: bool = Field(..., description="操作是否成功")
    task_id: Optional[str] = Field(None, description="任务ID")
    message: str = Field(..., description="响应消息")
    vlc_value: Optional[int] = Field(None, description="VLC值")
