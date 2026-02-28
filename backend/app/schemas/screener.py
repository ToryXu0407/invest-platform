from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class ScreenerRequest(BaseModel):
    """选股器请求"""
    # 估值指标
    pe_min: Optional[Decimal] = Field(None, description="PE 最小值")
    pe_max: Optional[Decimal] = Field(None, description="PE 最大值")
    pb_min: Optional[Decimal] = Field(None, description="PB 最小值")
    pb_max: Optional[Decimal] = Field(None, description="PB 最大值")
    pe_percentile_max: Optional[Decimal] = Field(None, description="PE 百分位最大值")
    pb_percentile_max: Optional[Decimal] = Field(None, description="PB 百分位最大值")
    
    # 股息率
    dividend_yield_min: Optional[Decimal] = Field(None, description="股息率最小值 (%)")
    
    # 财务指标
    roe_min: Optional[Decimal] = Field(None, description="ROE 最小值 (%)")
    revenue_growth_min: Optional[Decimal] = Field(None, description="营收增长率最小值 (%)")
    profit_growth_min: Optional[Decimal] = Field(None, description="净利润增长率最小值 (%)")
    
    # 市值
    market_cap_min: Optional[Decimal] = Field(None, description="最小市值 (亿)")
    market_cap_max: Optional[Decimal] = Field(None, description="最大市值 (亿)")
    
    # 市场
    markets: Optional[List[str]] = Field(None, description="市场列表：[\"A 股\", \"港股\"]")
    
    # 行业
    industries: Optional[List[str]] = Field(None, description="行业列表")


class ScreenerResult(BaseModel):
    """选股结果"""
    code: str
    name: str
    market: str
    industry: Optional[str] = None
    current_price: Decimal
    pe_ttm: Optional[Decimal] = None
    pb: Optional[Decimal] = None
    dividend_yield: Optional[Decimal] = None
    roe: Optional[Decimal] = None


class ScreenerResponse(BaseModel):
    """选股器响应"""
    data: List[ScreenerResult]
    total: int
    conditions: dict
