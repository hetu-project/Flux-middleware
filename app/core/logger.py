import logging
import sys
from typing import Optional
from app.core.config import get_settings

settings = get_settings()

class Logger:
    """日志配置类"""
    
    @staticmethod
    def setup_logger(
        name: str = "hetu_middleware",
        level: str = "INFO",
        format_string: Optional[str] = None
    ) -> logging.Logger:
        """
        设置日志配置
        
        Args:
            name: 日志器名称
            level: 日志级别
            format_string: 自定义格式字符串
            
        Returns:
            logging.Logger: 配置好的日志器
        """
        # 创建日志器
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
            
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        # 设置日志格式
        if format_string is None:
            format_string = (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(message)s"
            )
        
        formatter = logging.Formatter(format_string)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到日志器
        logger.addHandler(console_handler)
        
        return logger

# 创建默认日志器
logger = Logger.setup_logger()
