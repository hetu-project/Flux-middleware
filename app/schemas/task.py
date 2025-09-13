from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class TaskCreate(BaseModel):
    """创建任务的请求模型"""
    project_name: str = Field(..., description="项目名称")
    project_description: Optional[str] = Field(None, description="项目描述")
    project_icon: Optional[str] = Field(None, description="项目图标URL")
    task_type: str = Field(..., description="任务类型")
    twitter_name: str = Field(..., description="Twitter 用户名")
    twitter_url: HttpUrl = Field(..., description="Twitter URL")
    user_wallet: Optional[str] = Field(None, description="用户钱包地址")

class TaskResponse(BaseModel):
    """任务创建响应"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    task_id: Optional[str] = Field(None, description="任务ID（成功时返回）")
