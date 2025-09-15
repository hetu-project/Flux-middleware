from typing import Dict
from sqlalchemy.orm import Session
import re
from app.schemas.task import TaskCreate, TaskListResponse, TaskInfo, ProjectInfo
from app.schemas.flux import FluxTaskCreateRequest
from app.crud.project import ProjectCRUD
from app.crud.task import TaskCRUD
from app.services.twitter import TwitterService
from app.services.flux import FluxService
from fastapi import HTTPException
from app.utils import Utils
from app.core.logger import logger
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
            logger.info(f"开始创建任务: project_name={task_data.project_name}, twitter_name={task_data.twitter_name}")
            
            # 检查项目是否已存在
            existing_project = ProjectCRUD.get_project_by_name(db, task_data.project_name)
            if existing_project:
                logger.warning(f"项目已存在: {task_data.project_name}")
                raise HTTPException(
                    status_code=409,
                    detail=f"Project {task_data.project_name} already exists"
                )
            
            # 创建项目
            logger.info(f"创建项目: {task_data.project_name}")
            project = ProjectCRUD.create_project(
                db=db,
                name=task_data.project_name,
                description=task_data.project_description,
                icon=task_data.project_icon
            )
            
            # 刷新会话以获取项目ID
            db.flush()
            logger.info(f"项目创建成功: project_id={project.id}")
            
            # 创建任务
            logger.info(f"创建任务: twitter_name={task_data.twitter_name}, task_type={task_data.task_type}")
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
            logger.info(f"任务创建成功: task_id={task.task_id}")
            # 调用 Twitter 服务
            # 从 Twitter URL 中提取 tweet_id
            tweet_id = Utils.extract_tweet_id(str(task_data.twitter_url))
            logger.info(f"提取 tweet_id: {tweet_id}")
            
            try:
                from app.schemas.twitter import SubnetTweetTaskRequest
                
                # 创建任务请求数据
                task_request = SubnetTweetTaskRequest(
                    media_account=task_data.twitter_name,
                    tweet_id=tweet_id,
                    update_frequency="10 minutes"  
                )
                
                logger.info(f"调用 Twitter 服务: media_account={task_data.twitter_name}, tweet_id={tweet_id}")
                # 调用 Twitter 服务并获取返回结果
                twitter_response = await TwitterService.subnet_tweet_task(
                    method="POST",
                    task_data=task_request
                )
                
                logger.info(f"Twitter 服务响应: success={twitter_response.success}, message={twitter_response.message}")
                
                # 检查 Twitter 服务是否成功
                if not twitter_response.success:
                    logger.error(f"Twitter 服务失败: {twitter_response.message}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Twitter service failed: {twitter_response.message}"
                    )
                logger.info("Twitter 服务调用成功")
            except Exception as e:
                # 如果 Twitter 服务调用失败，回滚数据库操作
                logger.error(f"Twitter 服务调用异常: {str(e)}")
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process Twitter task: {str(e)}"
                )
            
            # 调用 Flux 服务
            try:
                # 从 Twitter URL 中提取 tweet_id
                tweet_id = Utils.extract_tweet_id(str(task_data.twitter_url))
                
                # 创建 Flux 任务请求
                flux_request = FluxTaskCreateRequest(
                    user_wallet=task_data.user_wallet or "",  # 如果没有提供钱包地址，使用空字符串
                    project_name=task_data.project_name,
                    project_icon=task_data.project_icon,
                    description=task_data.project_description or "",  # 使用项目描述，如果没有则使用空字符串
                    twitter_username=task_data.twitter_name,
                    twitter_link=task_data.twitter_url,
                    tweet_id=tweet_id,
                    task_type=task_data.task_type
                )
                
                logger.info(f"调用 Flux 服务: project_name={task_data.project_name}, user_wallet={task_data.user_wallet}")
                # 调用 Flux 服务
                flux_response = await FluxService.create_task(flux_request)
                
                logger.info(f"Flux 服务响应: success={flux_response.success}, message={flux_response.message}")
                
                if flux_response.success:
                    # Flux 服务成功，提交数据库事务
                    db.commit()
                    logger.info(f"任务创建完全成功: task_id={task.task_id}, flux_task_id={flux_response.task_id}")
                    return {
                        "success": True,
                        "message": f"Successfully created project {project.name} and Flux task",
                        "task_id": str(task.task_id),
                        "flux_task_id": flux_response.task_id,
                        "vlc_value": flux_response.vlc_value
                    }
                else:
                    # Flux 服务失败，回滚数据库操作
                    logger.error(f"Flux 服务失败: {flux_response.message}")
                    db.rollback()
                    raise HTTPException(
                        status_code=500,
                        detail=f"Flux service failed: {flux_response.message}"
                    )
                    
            except Exception as e:
                # Flux 服务调用异常，回滚数据库操作
                logger.error(f"Flux 服务调用异常: {str(e)}")
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=f"Flux service error: {str(e)}"
                )
            
        except HTTPException as e:
            db.rollback()
            # 重新抛出 HTTPException 以保持正确的状态码
            raise e
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}",
                "task_id": None
            }
    
    @staticmethod
    def get_tasks_list(
        db: Session,
        limit: int = 10,
        offset: int = 0
    ) -> TaskListResponse:
        """
        获取所有任务列表（带分页）
        
        Args:
            db: 数据库会话
            limit: 每页数量
            offset: 偏移量
            
        Returns:
            TaskListResponse: 任务列表响应
        """
        try:
            logger.info(f"获取任务列表: limit={limit}, offset={offset}")
            # 获取任务数据和总数
            tasks, total_count = TaskCRUD.get_tasks_with_pagination(
                db=db,
                limit=limit,
                offset=offset
            )
            logger.info(f"查询到 {len(tasks)} 个任务，总数: {total_count}")
            
            # 转换为响应格式
            task_list = []
            for task in tasks:
                # 构建项目信息
                project_info = ProjectInfo(
                    id=task.project.id,
                    name=task.project.name,
                    description=task.project.description,
                    icon=task.project.icon,
                    created_time=task.project.created_time
                )
                
                # 构建任务信息
                task_info = TaskInfo(
                    task_id=task.task_id,
                    twitter_name=task.twitter_name,
                    description=task.description,
                    type=task.type,
                    url=task.url,
                    user_wallet=task.user_wallet,
                    created_time=task.created_time,
                    project=project_info
                )
                task_list.append(task_info)
            
            # 计算是否还有更多数据
            has_more = (offset + limit) < total_count
            
            logger.info(f"任务列表返回: 返回 {len(task_list)} 个任务, has_more={has_more}")
            return TaskListResponse(
                tasks=task_list,
                total_count=total_count,
                limit=limit,
                offset=offset,
                has_more=has_more
            )
            
        except Exception as e:
            logger.error(f"获取任务列表失败: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get tasks list: {str(e)}"
            )
