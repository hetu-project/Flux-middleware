from pydantic import BaseModel, Field, HttpUrl

class TaskCreate(BaseModel):
    """创建任务的请求模型"""
    address: str = Field(..., description="用户地址")
    task_type: str = Field(..., description="任务类型")
    twitter_url: HttpUrl = Field(..., description="Twitter URL")

class TaskResponse(BaseModel):
    """任务创建响应"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    task_id: str = Field(..., description="任务ID")
