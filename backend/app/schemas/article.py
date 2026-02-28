from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ArticleBase(BaseModel):
    """文章基础模式"""
    title: str = Field(..., max_length=500)
    content: str
    summary: Optional[str] = None


class ArticleResponse(ArticleBase):
    """文章响应"""
    id: str
    author: Optional[str] = None
    source_url: Optional[str] = None
    series: Optional[str] = None
    published_at: Optional[datetime] = None
    view_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """文章列表响应"""
    data: list[ArticleResponse]
    total: int
    page: int
    page_size: int


class ArticleCreate(ArticleBase):
    """文章创建"""
    author: Optional[str] = None
    source_url: Optional[str] = None
    series: Optional[str] = None
    published_at: Optional[datetime] = None


class ArticleUpdate(BaseModel):
    """文章更新"""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    series: Optional[str] = None
