from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.schemas.stock import StockResponse, StockListResponse
from app.services.stock_service import StockService

router = APIRouter()


@router.get("", response_model=StockListResponse)
async def get_stocks(
    q: Optional[str] = Query(None, description="搜索关键词（代码/名称）"),
    market: Optional[str] = Query(None, description="市场：A 股/港股/美股"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """获取股票列表"""
    stock_service = StockService(db)
    stocks, total = await stock_service.list_stocks(
        search=q, market=market, page=page, page_size=page_size
    )
    return StockListResponse(data=stocks, total=total, page=page, page_size=page_size)


@router.get("/{code}", response_model=StockResponse)
async def get_stock(code: str, db: AsyncSession = Depends(get_db)):
    """获取股票详情"""
    stock_service = StockService(db)
    stock = await stock_service.get_stock_by_code(code)
    if not stock:
        raise HTTPException(status_code=404, detail="股票不存在")
    return stock


@router.get("/{code}/daily")
async def get_stock_daily_data(
    code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """获取股票日线数据"""
    stock_service = StockService(db)
    data = await stock_service.get_daily_data(code, start_date, end_date)
    return {"data": data}


@router.get("/{code}/indicators")
async def get_stock_indicators(code: str, db: AsyncSession = Depends(get_db)):
    """获取股票核心指标（PE/PB/股息率等）"""
    stock_service = StockService(db)
    indicators = await stock_service.get_indicators(code)
    if not indicators:
        raise HTTPException(status_code=404, detail="股票不存在")
    return indicators


@router.get("/{code}/financials")
async def get_stock_financials(code: str, db: AsyncSession = Depends(get_db)):
    """获取股票财务数据"""
    stock_service = StockService(db)
    financials = await stock_service.get_financials(code)
    return {"data": financials}
