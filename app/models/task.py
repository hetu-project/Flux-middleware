from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_name = Column(String(100), nullable=False)
    description = Column(Text,nullable=False)
    type = Column(String(50), nullable=False)  # 任务类型
    url = Column(String(255), nullable=False)  # 可能是 Twitter URL 或其他 URL
    user_wallet = Column(String(100))  # 用户钱包地址
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    
    # 外键关联
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    # 关系定义
    project = relationship("Project", back_populates="tasks")
