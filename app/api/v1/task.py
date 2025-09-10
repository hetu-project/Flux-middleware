from fastapi import APIRouter, HTTPException
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task import TaskService

router = APIRouter(tags=["task"])

@router.post("/create", response_model=TaskResponse)
async def create_task(task_data: TaskCreate) -> TaskResponse:
    """
    创建新的任务
    
    Args:
        task_data: 任务创建请求数据
        
    Returns:
        TaskResponse: 创建操作的响应
        
    Raises:
        HTTPException: 当创建操作失败时抛出
    """
    try:
        result = await TaskService.create_task(task_data)
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}"
        )
