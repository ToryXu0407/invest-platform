# Tushare 数据服务
# https://tushare.pro/document/2

import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings


class TushareService:
    """Tushare 数据服务"""
    
    def __init__(self):
        self.api_url = "http://api.tushare.pro"
        self.token = settings.TUSHARE_TOKEN
    
    async def _request(self, api_name: str, params: dict = None) -> dict:
        """发送请求到 Tushare API"""
        payload = {
            "api_name": api_name,
            "token": self.token,
            "params": params or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json=payload,
                timeout=30.0
            )
            result = response.json()
            
            if result.get('code') != 0:
                raise Exception(f"Tushare API Error: {result.get('msg')}")
            
            return result
    
    async def get_stock_list(self, market: str = 'A') -> List[Dict]:
        """
        获取股票列表
        
        Args:
            market: 市场类型 A-主板/科创板/创业板 B-科创板 C-创业板
            
        Returns:
            股票列表
        """
        result = await self._request('stock_basic', {
            'exchange': '',
            'list_status': 'L',  # 上市
            'fields': 'ts_code,symbol,name,area,industry,list_date,market'
        })
        
        stocks = []
        for item in result.get('data', {}).get('items', []):
            stocks.append({
                'ts_code': item[0],
                'symbol': item[1],
                'name': item[2],
                'area': item[3],
                'industry': item[4],
                'list_date': item[5],
                'market': item[6]
            })
        
        return stocks
    
    async def get_daily_data(
        self,
        ts_code: str,
        start_date: str,
        end_date: str
    ) -> List[Dict]:
        """
        获取日线数据
        
        Args:
            ts_code: 股票代码 (000001.SZ)
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
            
        Returns:
            日线数据列表
        """
        result = await self._request('daily', {
            'ts_code': ts_code,
            'start_date': start_date,
            'end_date': end_date
        })
        
        daily_data = []
        for item in result.get('data', {}).get('items', []):
            daily_data.append({
                'trade_date': item[1],
                'open': float(item[3]) if item[3] else None,
                'high': float(item[4]) if item[4] else None,
                'low': float(item[5]) if item[5] else None,
                'close': float(item[6]) if item[6] else None,
                'vol': float(item[9]) if item[9] else None,
                'amount': float(item[10]) if item[10] else None
            })
        
        return daily_data
    
    async def get_daily_basic(
        self,
        trade_date: str,
        ts_code: str = None
    ) -> List[Dict]:
        """
        获取每日指标（PE/PB/股息率等）
        
        Args:
            trade_date: 交易日期 (YYYYMMDD)
            ts_code: 股票代码（可选）
            
        Returns:
            每日指标数据
        """
        params = {'trade_date': trade_date}
        if ts_code:
            params['ts_code'] = ts_code
        
        result = await self._request('daily_basic', {
            **params,
            'fields': 'ts_code,trade_date,close,pe_ttm,pb,dv_ratio,total_mv'
        })
        
        indicators = []
        for item in result.get('data', {}).get('items', []):
            indicators.append({
                'ts_code': item[0],
                'trade_date': item[1],
                'close': float(item[2]) if item[2] else None,
                'pe_ttm': float(item[3]) if item[3] else None,
                'pb': float(item[4]) if item[4] else None,
                'dv_ratio': float(item[5]) if item[5] else None,  # 股息率
                'total_mv': float(item[6]) if item[6] else None  # 总市值
            })
        
        return indicators
    
    async def get_dividend(self, ts_code: str) -> List[Dict]:
        """
        获取分红数据
        
        Args:
            ts_code: 股票代码
            
        Returns:
            分红数据列表
        """
        result = await self._request('dividend', {
            'ts_code': ts_code,
            'fields': 'ts_code,ann_date,record_date,ex_date,pay_date,div_proc,close'
        })
        
        dividends = []
        for item in result.get('data', {}).get('items', []):
            dividends.append({
                'ts_code': item[0],
                'ann_date': item[1],
                'record_date': item[2],
                'ex_date': item[3],
                'pay_date': item[4],
                'div_proc': item[5],  # 分红方案
                'close': float(item[6]) if item[6] else None
            })
        
        return dividends
    
    async def get_fina_indicator(self, ts_code: str) -> List[Dict]:
        """
        获取财务指标数据
        
        Args:
            ts_code: 股票代码
            
        Returns:
            财务指标数据
        """
        result = await self._request('fina_indicator', {
            'ts_code': ts_code,
            'fields': 'ts_code,ann_date,end_date,roa,roe,sales_exp,op_profit,n_income,'
                     'operate_cash_invest,operate_cash_finance,operate_cash_oper'
        })
        
        indicators = []
        for item in result.get('data', {}).get('items', []):
            indicators.append({
                'ts_code': item[0],
                'ann_date': item[1],
                'end_date': item[2],
                'roa': float(item[3]) if item[3] else None,
                'roe': float(item[4]) if item[4] else None,
                'sales_exp': float(item[5]) if item[5] else None,  # 营收
                'op_profit': float(item[6]) if item[6] else None,  # 营业利润
                'n_income': float(item[7]) if item[7] else None,  # 净利润
                'operate_cash_invest': float(item[8]) if item[8] else None,
                'operate_cash_finance': float(item[9]) if item[9] else None,
                'operate_cash_oper': float(item[10]) if item[10] else None  # 经营现金流
            })
        
        return indicators
    
    async def get_income(self, ts_code: str) -> List[Dict]:
        """
        获取利润表数据
        
        Args:
            ts_code: 股票代码
            
        Returns:
            利润表数据
        """
        result = await self._request('income', {
            'ts_code': ts_code,
            'fields': 'ts_code,ann_date,end_date,total_revenue,operating_profit,'
                     'net_profit_attributable'
        })
        
        incomes = []
        for item in result.get('data', {}).get('items', []):
            incomes.append({
                'ts_code': item[0],
                'ann_date': item[1],
                'end_date': item[2],
                'total_revenue': float(item[3]) if item[3] else None,
                'operating_profit': float(item[4]) if item[4] else None,
                'net_profit': float(item[5]) if item[5] else None
            })
        
        return incomes


# 单例
tushare_service = TushareService()
