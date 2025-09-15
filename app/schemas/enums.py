from enum import Enum

class TaskType(str, Enum):
    """任务类型枚举"""
    TWITTER_RETWEET = "twitter_retweet"