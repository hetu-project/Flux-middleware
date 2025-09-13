from typing import Dict
from sqlalchemy.orm import Session
import re
from app.schemas.task import TaskCreate
from app.schemas.flux import FluxTaskCreateRequest
from app.crud.project import ProjectCRUD
from app.crud.task import TaskCRUD
from app.services.twitter import TwitterService
from app.services.flux import FluxService
from fastapi import HTTPException
from app.utils import Utils
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
                twitter_name=task_data.twitter_name,
                twitter_url=str(task_data.twitter_url),
                user_wallet=task_data.user_wallet
            )
            
            # 刷新会话以获取任务ID
            db.flush()
            db.refresh(task)
            # 暂时注释掉 Twitter 服务调用逻辑
            # 从 Twitter URL 中提取 tweet_id
            tweet_id = Utils.extract_tweet_id(str(task_data.twitter_url))
            # 调用 Twitter 服务
            # try:
            #     from app.schemas.twitter import SubnetTweetTaskRequest
            #     
            #     # 创建任务请求数据
            #     task_request = SubnetTweetTaskRequest(
            #         media_account=task_data.twitter_name,
            #         tweet_id=tweet_id,
            #         update_frequency="6 hours"  
            #     )
            #     
            #     # 调用 Twitter 服务并获取返回结果
            #     twitter_response = await TwitterService.subnet_tweet_task(
            #         method="POST",
            #         task_data=task_request
            #     )
            #     
            #     # 打印 Twitter 服务的返回结果
            #     print(f"Twitter service response: {twitter_response}")
            #     
            #     # 检查 Twitter 服务是否成功
            #     if not twitter_response.success:
            #         raise HTTPException(
            #             status_code=500,
            #             detail=f"Twitter service failed: {twitter_response.message}"
            #         )
            # except Exception as e:
            #     # 如果 Twitter 服务调用失败，回滚数据库操作
            #     db.rollback()
            #     raise HTTPException(
            #         status_code=500,
            #         detail=f"Failed to process Twitter task: {str(e)}"
            #     )
            
            # 调用 Flux 服务
            try:
                # 从 Twitter URL 中提取 tweet_id
                tweet_id = Utils.extract_tweet_id(str(task_data.twitter_url))
                
                # 创建 Flux 任务请求
                flux_request = FluxTaskCreateRequest(
                    user_wallet=task_data.user_wallet or "",  # 如果没有提供钱包地址，使用空字符串
                    project_name=task_data.project_name,
                    project_icon=task_data.project_icon,
                    description="",  # 传递空字符串
                    twitter_username=task_data.twitter_name,
                    twitter_link=task_data.twitter_url,
                    tweet_id=tweet_id
                )
                
                # 调用 Flux 服务
                flux_response = await FluxService.create_task(flux_request)
                
                if flux_response.success:
                    # Flux 服务成功，提交数据库事务
                    db.commit()
                    return {
                        "success": True,
                        "message": f"Successfully created project {project.name} and Flux task",
                        "task_id": str(task.task_id),
                        "flux_task_id": flux_response.task_id,
                        "vlc_value": flux_response.vlc_value
                    }
                else:
                    # Flux 服务失败，回滚数据库操作
                    db.rollback()
                    return {
                        "success": False,
                        "message": f"Flux service failed: {flux_response.message}",
                        "task_id": None
                    }
                    
            except Exception as e:
                # Flux 服务调用异常，回滚数据库操作
                db.rollback()
                return {
                    "success": False,
                    "message": f"Flux service error: {str(e)}",
                    "task_id": None
                }
            
        except HTTPException as e:
            db.rollback()
            return {
                "success": False,
                "message": e.detail,
                "task_id": None
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}",
                "task_id": None
            }
