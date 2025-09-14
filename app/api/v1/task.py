from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskResponse, TaskListRequest, TaskListResponse
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
        # 重新抛出 HTTPException 以返回正确的状态码
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create task: {str(e)}"
        )

@router.post("/list", response_model=TaskListResponse)
async def get_tasks_list(
    request: TaskListRequest,
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    获取所有任务列表（带分页）
    
    Args:
        request: 任务列表请求数据
        db: 数据库会话
        
    Returns:
        TaskListResponse: 任务列表响应
        
    Raises:
        HTTPException: 当获取操作失败时抛出
    """
    try:
        return TaskService.get_tasks_list(db=db, limit=request.limit, offset=request.offset)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get tasks list: {str(e)}"
        )