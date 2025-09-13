from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task import TaskService
from app.db.base import get_db

router = APIRouter(tags=["task"])

@router.post("/create", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    创建新的任务和相关项目
    
    Args:
        task_data: 任务创建请求数据
        db: 数据库会话
        
    Returns:
        TaskResponse: 创建操作的响应
        
    Raises:
        HTTPException: 当创建操作失败时抛出
    """
    try:
        result = await TaskService.create_task(db, task_data)
        return TaskResponse(**result)
    except HTTPException as e:
        return TaskResponse(
            success=False,
            message=e.detail,
            task_id=None
        )
    except Exception as e:
        return TaskResponse(
            success=False,
            message=f"Failed to create task: {str(e)}",
            task_id=None
        )