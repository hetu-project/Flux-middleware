from sqlalchemy.orm import Session
from app.models.task import Task
from typing import Optional

class TaskCRUD:
    @staticmethod
    def create_task(
        db: Session,
        project_id: int,
        task_type: str,
        twitter_url: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """
        创建任务但不提交
        
        Args:
            db: 数据库会话
            project_id: 项目ID
            task_type: 任务类型
            twitter_url: Twitter URL
            name: 任务名称（可选）
            description: 任务描述（可选）
            
        Returns:
            Task: 创建的任务对象（未提交）
        """
        # 如果没有提供任务名称，使用 Twitter URL
        if not name:
            name = f"Twitter Task: {twitter_url}"
            
        db_task = Task(
            project_id=project_id,
            twitter_name=name,
            description=description,
            type=task_type,
            url=twitter_url
        )
        db.add(db_task)
        return db_task
