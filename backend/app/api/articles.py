from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.schemas.article import ArticleListResponse, ArticleResponse
from app.services.article_service import ArticleService

router = APIRouter()


@router.get("", response_model=ArticleListResponse)
async def get_articles(
    q: Optional[str] = Query(None, description="搜索关键词"),
    series: Optional[str] = Query(None, description="系列：天阶功法/地阶功法/玄阶功法"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取文章列表"""
    article_service = ArticleService(db)
    articles, total = await article_service.list_articles(
        search=q, series=series, page=page, page_size=page_size
    )
    return ArticleListResponse(data=articles, total=total, page=page, page_size=page_size)


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: str, db: AsyncSession = Depends(get_db)):
    """获取文章详情"""
    article_service = ArticleService(db)
    article = await article_service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article


@router.get("/search")
async def search_articles(
    q: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """全文搜索文章"""
    article_service = ArticleService(db)
    results = await article_service.search_articles(q, page, page_size)
    return results
