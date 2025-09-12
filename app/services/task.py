from typing import Dict
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate
from app.crud.project import ProjectCRUD
from app.crud.task import TaskCRUD
from fastapi import HTTPException

class TaskService:
    """任务服务"""
    
    @staticmethod
    async def create_task(db: Session, task_data: TaskCreate) -> Dict[str, bool | str]:
        """
        创建任务和项目
        
        Args:
            db: 数据库会话
            task_data: 任务创建请求数据
            
        Returns:
            Dict[str, bool | str]: 包含操作结果和消息的字典
            
        Raises:
            HTTPException: 当项目已存在时抛出
        """
        try:
            # 检查项目是否已存在
            existing_project = ProjectCRUD.get_project_by_name(db, task_data.project_name)
            if existing_project:
                raise HTTPException(
                    status_code=400,
                    detail=f"Project {task_data.project_name} already exists"
                )
            
            # 创建项目
            project = ProjectCRUD.create_project(
                db=db,
                name=task_data.project_name,
                description=task_data.project_description,
                icon=task_data.project_icon
            )
            
            # 刷新会话以获取项目ID
            db.flush()
            
            # 创建任务
            task = TaskCRUD.create_task(
                db=db,
                project_id=project.id,
                task_type=task_data.task_type,
                twitter_url=str(task_data.twitter_url)
            )
            
            # 提交事务
            db.commit()
            
            # 刷新会话以获取任务ID
            db.refresh(task)
            
            return {
                "success": True,
                "message": f"Successfully created project {project.name} and associated task",
                "task_id": str(task.task_id)
            }
            
        except HTTPException as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create task: {str(e)}"
            )
