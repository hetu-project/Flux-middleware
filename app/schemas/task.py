from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

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

class ProjectInfo(BaseModel):
    """项目信息"""
    id: int = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")
    icon: Optional[str] = Field(None, description="项目图标URL")
    created_time: datetime = Field(..., description="创建时间")

class TaskInfo(BaseModel):
    """任务信息"""
    task_id: int = Field(..., description="任务ID")
    twitter_name: str = Field(..., description="Twitter用户名")
    description: Optional[str] = Field(None, description="任务描述")
    type: str = Field(..., description="任务类型")
    url: str = Field(..., description="任务URL")
    user_wallet: Optional[str] = Field(None, description="用户钱包地址")
    created_time: datetime = Field(..., description="创建时间")
    project: ProjectInfo = Field(..., description="关联的项目信息")

class TaskListRequest(BaseModel):
    """任务列表请求"""
    limit: int = Field(10, ge=1, le=100, description="每页数量")
    offset: int = Field(0, ge=0, description="偏移量")

class TaskListResponse(BaseModel):
    """任务列表响应"""
    tasks: List[TaskInfo] = Field(..., description="任务列表")
    total_count: int = Field(..., description="总数量")
    limit: int = Field(..., description="每页数量")
    offset: int = Field(..., description="偏移量")
    has_more: bool = Field(..., description="是否还有更多数据")
