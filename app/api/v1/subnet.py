from fastapi import APIRouter, HTTPException
from app.schemas.subnet import SubnetCreate, SubnetResponse
from app.services.subnet import SubnetService

router = APIRouter(tags=["subnet"])

@router.post("/create", response_model=SubnetResponse)
async def create_subnet(subnet_data: SubnetCreate) -> SubnetResponse:
    """
    创建新的子网
    
    Args:
        subnet_data: 子网创建请求数据
        
    Returns:
        SubnetResponse: 创建操作的响应
        
    Raises:
        HTTPException: 当创建操作失败时抛出
    """
    try:
        result = await SubnetService.create_subnet(subnet_data)
        return SubnetResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create subnet: {str(e)}"
        )
