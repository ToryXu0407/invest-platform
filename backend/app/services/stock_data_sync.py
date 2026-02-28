# 股票数据同步服务

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging

from app.models.stock import Stock, StockDailyData, StockFinancial
from app.services.data_sources.tushare_service import tushare_service
from app.services.data_sources.akshare_service import akshare_service
from app.services.indicator_calculator import indicator_calculator

logger = logging.getLogger(__name__)


class StockDataSyncService:
    """股票数据同步服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def sync_stock_list(self) -> int:
        """
        同步股票列表
        
        Returns:
            同步的股票数量
        """
        try:
            # 从 Tushare 获取股票列表
            stock_list = await tushare_service.get_stock_list()
            
            count = 0
            for stock_data in stock_list:
                # 检查是否已存在
                result = await self.db.execute(
                    select(Stock).where(Stock.code == stock_data['symbol'])
                )
                stock = result.scalar_one_or_none()
                
                if stock:
                    # 更新
                    stock.name = stock_data['name']
                    stock.industry = stock_data['industry']
                    stock.listed_date = self._parse_date(stock_data['list_date'])
                    stock.market = self._convert_market(stock_data['market'])
                else:
                    # 创建
                    stock = Stock(
                        code=stock_data['symbol'],
                        name=stock_data['name'],
                        market=self._convert_market(stock_data['market']),
                        industry=stock_data['industry'],
                        listed_date=self._parse_date(stock_data['list_date']),
                    )
                    self.db.add(stock)
                
                count += 1
            
            await self.db.commit()
            logger.info(f"同步股票列表完成，共 {count} 只股票")
            return count
            
        except Exception as e:
            logger.error(f"同步股票列表失败：{e}")
            await self.db.rollback()
            return 0
    
    async def sync_daily_data(
        self,
        stock_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> int:
        """
        同步日线数据
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            同步的数据条数
        """
        try:
            # 获取股票
            result = await self.db.execute(
                select(Stock).where(Stock.code == stock_code)
            )
            stock = result.scalar_one_or_none()
            
            if not stock:
                logger.warning(f"股票 {stock_code} 不存在")
                return 0
            
            # 默认同步最近 1 年数据
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            # 从 Tushare 获取日线数据
            daily_data = await tushare_service.get_daily_data(
                ts_code=self._convert_ts_code(stock_code),
                start_date=start_date,
                end_date=end_date
            )
            
            # 获取每日指标数据
            indicators = await tushare_service.get_daily_basic(
                trade_date=end_date,
                ts_code=self._convert_ts_code(stock_code)
            )
            
            # 构建指标映射
            indicator_map = {}
            for ind in indicators:
                indicator_map[ind['trade_date']] = ind
            
            count = 0
            for data in daily_data:
                # 检查是否已存在
                result = await self.db.execute(
                    select(StockDailyData).where(
                        and_(
                            StockDailyData.stock_id == stock.id,
                            StockDailyData.date == self._parse_date(data['trade_date'])
                        )
                    )
                )
                daily = result.scalar_one_or_none()
                
                # 获取当日指标
                ind = indicator_map.get(data['trade_date'], {})
                
                if daily:
                    # 更新
                    daily.open = data['open']
                    daily.high = data['high']
                    daily.low = data['low']
                    daily.close = data['close']
                    daily.volume = data['vol']
                    daily.amount = data['amount']
                    daily.pe_ttm = ind.get('pe_ttm')
                    daily.pb = ind.get('pb')
                    daily.dividend_yield = ind.get('dv_ratio')
                else:
                    # 创建
                    daily = StockDailyData(
                        stock_id=stock.id,
                        date=self._parse_date(data['trade_date']),
                        open=data['open'],
                        high=data['high'],
                        low=data['low'],
                        close=data['close'],
                        volume=data['vol'],
                        amount=data['amount'],
                        pe_ttm=ind.get('pe_ttm'),
                        pb=ind.get('pb'),
                        dividend_yield=ind.get('dv_ratio'),
                    )
                    self.db.add(daily)
                
                count += 1
            
            await self.db.commit()
            logger.info(f"同步 {stock_code} 日线数据完成，共 {count} 条")
            return count
            
        except Exception as e:
            logger.error(f"同步 {stock_code} 日线数据失败：{e}")
            await self.db.rollback()
            return 0
    
    async def sync_financials(self, stock_code: str) -> int:
        """
        同步财务数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            同步的数据条数
        """
        try:
            # 获取股票
            result = await self.db.execute(
                select(Stock).where(Stock.code == stock_code)
            )
            stock = result.scalar_one_or_none()
            
            if not stock:
                logger.warning(f"股票 {stock_code} 不存在")
                return 0
            
            # 从 Tushare 获取财务指标
            fina_indicators = await tushare_service.get_fina_indicator(
                ts_code=self._convert_ts_code(stock_code)
            )
            
            count = 0
            for ind in fina_indicators:
                # 检查是否已存在
                result = await self.db.execute(
                    select(StockFinancial).where(
                        and_(
                            StockFinancial.stock_id == stock.id,
                            StockFinancial.report_date == self._parse_date(ind['end_date'])
                        )
                    )
                )
                financial = result.scalar_one_or_none()
                
                if financial:
                    # 更新
                    financial.roe = ind['roe']
                    financial.revenue = ind['sales_exp']
                    financial.net_profit = ind['n_income']
                    financial.operating_cash_flow = ind['operate_cash_oper']
                else:
                    # 创建
                    financial = StockFinancial(
                        stock_id=stock.id,
                        report_date=self._parse_date(ind['end_date']),
                        report_type='quarterly',  # 季报
                        revenue=ind['sales_exp'],
                        net_profit=ind['n_income'],
                        operating_cash_flow=ind['operate_cash_oper'],
                        roe=ind['roe'],
                    )
                    self.db.add(financial)
                
                count += 1
            
            await self.db.commit()
            logger.info(f"同步 {stock_code} 财务数据完成，共 {count} 条")
            return count
            
        except Exception as e:
            logger.error(f"同步 {stock_code} 财务数据失败：{e}")
            await self.db.rollback()
            return 0
    
    def _convert_market(self, market: str) -> str:
        """转换市场类型"""
        market_map = {
            '主板': 'A 股',
            '科创板': 'A 股',
            '创业板': 'A 股',
            '中小板': 'A 股',
            'B 股': 'B 股',
        }
        return market_map.get(market, 'A 股')
    
    def _convert_ts_code(self, code: str) -> str:
        """转换股票代码为 Tushare 格式"""
        # 简单转换，实际需要根据市场判断
        if code.startswith('6'):
            return f"{code}.SH"
        else:
            return f"{code}.SZ"
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        
        try:
            # 尝试不同格式
            for fmt in ['%Y%m%d', '%Y-%m-%d', '%Y/%m/%d']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        except Exception:
            return None


# 工厂函数
def get_stock_data_sync_service(db: AsyncSession) -> StockDataSyncService:
    """获取数据同步服务实例"""
    return StockDataSyncService(db)
