from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.schemas.screener import ScreenerRequest, ScreenerResponse
from app.services.screener_service import ScreenerService

router = APIRouter()


@router.post("", response_model=ScreenerResponse)
async def screen_stocks(
    request: ScreenerRequest,
    db: AsyncSession = Depends(get_db),
):
    """选股器 - 多条件筛选股票"""
    screener_service = ScreenerService(db)
    results = await screener_service.screen(request)
    return ScreenerResponse(
        data=results,
        total=len(results),
        conditions=request.dict(),
    )


@router.get("/presets")
async def get_screener_presets():
    """获取预设选股模板"""
    presets = [
        {
            "id": "high_dividend",
            "name": "高股息策略",
            "description": "股息率 > 5%, PE < 20, 连续 3 年分红",
            "conditions": {
                "dividend_yield_min": 5,
                "pe_max": 20,
            }
        },
        {
            "id": "low_valuation",
            "name": "低估值策略",
            "description": "PE 百分位 < 20%, PB 百分位 < 20%",
            "conditions": {
                "pe_percentile_max": 20,
                "pb_percentile_max": 20,
            }
        },
        {
            "id": "quality_growth",
            "name": "优质成长策略",
            "description": "ROE > 15%, 营收增长率 > 20%",
            "conditions": {
                "roe_min": 15,
                "revenue_growth_min": 20,
            }
        },
    ]
    return {"presets": presets}
