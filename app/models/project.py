from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    icon = Column(String(255))  # URL for the icon
    description = Column(Text)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系定义
    tasks = relationship("Task", back_populates="project")
