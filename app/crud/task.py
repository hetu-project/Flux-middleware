from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.task import Task
from app.models.project import Project
from typing import Optional, List, Tuple

class TaskCRUD:
    @staticmethod
    def create_task(
        db: Session,
        project_id: int,
        task_type: str,
        twitter_name: str,
        twitter_url: str,
        description: Optional[str] = None,
        user_wallet: Optional[str] = None,
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
            user_wallet: 用户钱包地址（可选）
            
        Returns:
            Task: 创建的任务对象（未提交）
        """
        db_task = Task(
            project_id=project_id,
            twitter_name=twitter_name,
            description=description,
            type=task_type,
            url=twitter_url,
            user_wallet=user_wallet
        )
        db.add(db_task)
        return db_task
    
    @staticmethod
    def get_tasks_with_pagination(
        db: Session,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[Task], int]:
        """
        获取所有任务（带分页）
        
        Args:
            db: 数据库会话
            limit: 每页数量
            offset: 偏移量
            
        Returns:
            Tuple[List[Task], int]: (任务列表, 总数量)
        """
        # 获取总数
        total_count = db.query(func.count(Task.task_id)).scalar()
        
        # 获取分页数据，包含关联的 project 信息
        tasks = db.query(Task).join(Project).offset(offset).limit(limit).all()
        
        return tasks, total_count
