from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Tuple, List, Dict
from datetime import datetime, timedelta
from app.models.stock import Stock, StockDailyData, StockFinancial
from app.schemas.stock import StockResponse, StockIndicators
from app.services.indicator_calculator import indicator_calculator


class StockService:
    """股票服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def list_stocks(
        self,
        search: Optional[str] = None,
        market: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Stock], int]:
        """获取股票列表"""
        query = select(Stock)
        
        if search:
            query = query.where(
                (Stock.code.ilike(f"%{search}%")) | (Stock.name.ilike(f"%{search}%"))
            )
        
        if market:
            query = query.where(Stock.market == market)
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # 分页
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        stocks = result.scalars().all()
        
        return stocks, total
    
    async def get_stock_by_code(self, code: str) -> Optional[Stock]:
        """获取股票详情"""
        result = await self.db.execute(select(Stock).where(Stock.code == code))
        return result.scalar_one_or_none()
    
    async def get_daily_data(
        self,
        code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[dict]:
        """获取日线数据"""
        query = select(StockDailyData).join(Stock).where(Stock.code == code)
        
        if start_date:
            query = query.where(StockDailyData.date >= start_date)
        if end_date:
            query = query.where(StockDailyData.date <= end_date)
        
        query = query.order_by(StockDailyData.date.desc())
        result = await self.db.execute(query)
        data = result.scalars().all()
        
        return [
            {
                "date": d.date,
                "open": float(d.open) if d.open else None,
                "high": float(d.high) if d.high else None,
                "low": float(d.low) if d.low else None,
                "close": float(d.close) if d.close else None,
                "pe_ttm": float(d.pe_ttm) if d.pe_ttm else None,
                "pb": float(d.pb) if d.pb else None,
                "dividend_yield": float(d.dividend_yield) if d.dividend_yield else None,
            }
            for d in data
        ]
    
    async def get_indicators(self, code: str) -> Optional[StockIndicators]:
        """获取核心指标"""
        stock = await self.get_stock_by_code(code)
        if not stock:
            return None
        
        # 获取最新日线数据
        result = await self.db.execute(
            select(StockDailyData)
            .where(StockDailyData.stock_id == stock.id)
            .order_by(StockDailyData.date.desc())
            .limit(1)
        )
        daily = result.scalar_one_or_none()
        
        if not daily or not daily.close:
            return None
        
        # 获取历史 PE/PB 数据用于计算百分位
        pe_history = await self._get_pe_history(stock.id)
        pb_history = await self._get_pb_history(stock.id)
        
        # 计算百分位
        pe_percentile = None
        pb_percentile = None
        
        if daily.pe_ttm and pe_history:
            pe_percentile = indicator_calculator.calculate_percentile(
                float(daily.pe_ttm), pe_history, days=3650
            )
        
        if daily.pb and pb_history:
            pb_percentile = indicator_calculator.calculate_percentile(
                float(daily.pb), pb_history, days=3650
            )
        
        # 获取财务数据计算真钱指数
        true_money_index = await self._calculate_true_money_index(stock.id)
        
        return StockIndicators(
            code=stock.code,
            name=stock.name,
            current_price=float(daily.close),
            pe_ttm=float(daily.pe_ttm) if daily.pe_ttm else None,
            pb=float(daily.pb) if daily.pb else None,
            dividend_yield=float(daily.dividend_yield) if daily.dividend_yield else None,
            pe_percentile=pe_percentile,
            pb_percentile=pb_percentile,
            true_money_index=true_money_index,
        )
    
    async def _get_pe_history(self, stock_id: str, days: int = 3650) -> List[float]:
        """获取历史 PE 数据"""
        cutoff_date = datetime.now() - timedelta(days=days)
        result = await self.db.execute(
            select(StockDailyData.pe_ttm)
            .where(
                (StockDailyData.stock_id == stock_id) &
                (StockDailyData.date >= cutoff_date) &
                (StockDailyData.pe_ttm.isnot(None))
            )
        )
        return [float(row[0]) for row in result.fetchall() if row[0] and row[0] > 0]
    
    async def _get_pb_history(self, stock_id: str, days: int = 3650) -> List[float]:
        """获取历史 PB 数据"""
        cutoff_date = datetime.now() - timedelta(days=days)
        result = await self.db.execute(
            select(StockDailyData.pb)
            .where(
                (StockDailyData.stock_id == stock_id) &
                (StockDailyData.date >= cutoff_date) &
                (StockDailyData.pb.isnot(None))
            )
        )
        return [float(row[0]) for row in result.fetchall() if row[0] and row[0] > 0]
    
    async def _calculate_true_money_index(self, stock_id: str) -> Optional[float]:
        """计算真钱指数"""
        result = await self.db.execute(
            select(StockFinancial)
            .where(StockFinancial.stock_id == stock_id)
            .order_by(StockFinancial.report_date.desc())
            .limit(1)
        )
        financial = result.scalar_one_or_none()
        
        if not financial or not financial.net_profit or not financial.operating_cash_flow:
            return None
        
        return indicator_calculator.calculate_true_money_index(
            float(financial.operating_cash_flow),
            float(financial.net_profit)
        )
    
    async def get_financials(self, code: str) -> List[dict]:
        """获取财务数据"""
        stock = await self.get_stock_by_code(code)
        if not stock:
            return []
        
        result = await self.db.execute(
            select(StockFinancial)
            .where(StockFinancial.stock_id == stock.id)
            .order_by(StockFinancial.report_date.desc())
        )
        financials = result.scalars().all()
        
        return [
            {
                "report_date": f.report_date,
                "report_type": f.report_type,
                "revenue": float(f.revenue) if f.revenue else None,
                "net_profit": float(f.net_profit) if f.net_profit else None,
                "roe": float(f.roe) if f.roe else None,
            }
            for f in financials
        ]
