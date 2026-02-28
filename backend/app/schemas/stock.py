from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class StockBase(BaseModel):
    """股票基础模式"""
    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    market: str = Field(..., description="市场：A 股/港股/美股")


class StockResponse(StockBase):
    """股票响应"""
    id: str
    industry: Optional[str] = None
    sector: Optional[str] = None
    listed_date: Optional[date] = None
    status: str = "active"
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockListResponse(BaseModel):
    """股票列表响应"""
    data: list[StockResponse]
    total: int
    page: int
    page_size: int


class StockDailyData(BaseModel):
    """股票日线数据"""
    date: date
    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    close: Optional[Decimal] = None
    volume: Optional[int] = None
    pe_ttm: Optional[Decimal] = None
    pb: Optional[Decimal] = None
    dividend_yield: Optional[Decimal] = None


class StockIndicators(BaseModel):
    """股票核心指标"""
    code: str
    name: str
    current_price: Decimal
    dividend_yield: Optional[Decimal] = None
    pe_ttm: Optional[Decimal] = None
    pb: Optional[Decimal] = None
    pe_percentile: Optional[Decimal] = None
    pb_percentile: Optional[Decimal] = None
    true_money_index: Optional[Decimal] = None  # 真钱指数
