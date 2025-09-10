from pydantic import BaseModel, Field, HttpUrl

class SubnetCreate(BaseModel):
    """创建子网的请求模型"""
    name: str = Field(..., description="子网名称")
    description: str = Field(..., description="子网描述")
    twitter_url: HttpUrl = Field(..., description="Twitter URL")
    flux_reward: float = Field(..., gt=0, description="Flux 奖励数量")

class SubnetResponse(BaseModel):
    """子网创建响应模型"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
