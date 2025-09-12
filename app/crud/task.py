from sqlalchemy.orm import Session
from app.models.task import Task
from typing import Optional

class TaskCRUD:
    @staticmethod
    def create_task(
        db: Session,
        project_id: int,
        task_type: str,
        twitter_name: str,
        twitter_url: str,
        description: Optional[str] = None,
    ) -> Task:
        """
        创建任务但不提交
        
        Args:
            db: 数据库会话
            project_id: 项目ID
            task_type: 任务类型
            twitter_name: Twitter 用户名
            twitter_url: Twitter URL
            description: 任务描述（可选）
            
        Returns:
            Task: 创建的任务对象（未提交）
        """
        db_task = Task(
            project_id=project_id,
            twitter_name=twitter_name,
            description=description,
            type=task_type,
            url=twitter_url
        )
        db.add(db_task)
        return db_task
