import re
from fastapi import HTTPException

class Utils:
    @staticmethod
    def extract_tweet_id(twitter_url: str) -> str:
        """
        从 Twitter URL 中提取 tweet_id
        
        Args:
            twitter_url: Twitter 帖子 URL
            
        Returns:
            str: tweet_id
            
        Raises:
            HTTPException: 当 URL 格式不正确时抛出
        """
        # 获取 URL 最后一段
        post_id = twitter_url.split('/')[-1]
        
        # 检查是否为数字
        if not post_id.isdigit():
            raise HTTPException(
                status_code=400,
                detail="Invalid Twitter URL format. Expected format: https://x.com/username/status/tweet_id"
            )
            
        return post_id
