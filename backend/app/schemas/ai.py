from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str = Field(..., description="角色：user/assistant")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., description="用户消息")
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    message: str
    sources: Optional[List[str]] = None  # 引用来源
    created_at: datetime


class ChatHistory(BaseModel):
    """聊天历史"""
    id: str
    message: str
    response: str
    created_at: datetime
