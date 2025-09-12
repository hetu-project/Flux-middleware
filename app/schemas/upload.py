from pydantic import BaseModel, Field

class FileUploadResponse(BaseModel):
    """文件上传响应"""
    success: bool = Field(..., description="上传是否成功")
    message: str = Field(..., description="响应消息")
    file_url: str = Field(..., description="文件访问URL")
    file_name: str = Field(..., description="原始文件名")
    file_size: int = Field(..., description="文件大小（字节）")
