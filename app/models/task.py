from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)  # 任务类型
    url = Column(String(255), nullable=False)  # 可能是 Twitter URL 或其他 URL
    created_time = Column(DateTime(timezone=True), server_default=func.now())
