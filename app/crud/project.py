from sqlalchemy.orm import Session
from app.models.project import Project
from typing import Optional

class ProjectCRUD:
    @staticmethod
    def create_project(
        db: Session,
        name: str,
        description: Optional[str] = None,
        icon: Optional[str] = None
    ) -> Project:
        """
        创建项目但不提交
        
        Args:
            db: 数据库会话
            name: 项目名称
            description: 项目描述
            icon: 项目图标URL
            
        Returns:
            Project: 创建的项目对象（未提交）
        """
        db_project = Project(
            name=name,
            description=description,
            icon=icon
        )
        db.add(db_project)
        return db_project
        
    @staticmethod
    def get_project_by_name(db: Session, name: str) -> Optional[Project]:
        """
        通过名称查找项目
        
        Args:
            db: 数据库会话
            name: 项目名称
            
        Returns:
            Optional[Project]: 项目对象，如果不存在则返回 None
        """
        return db.query(Project).filter(Project.name == name).first()
