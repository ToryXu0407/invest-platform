# AkShare 数据服务（备用）
# https://akshare.akfamily.xyz/

import akshare as ak
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


class AkShareService:
    """AkShare 数据服务（备用数据源）"""
    
    def __init__(self):
        pass
    
    def get_stock_list(self) -> List[Dict]:
        """获取 A 股股票列表"""
        try:
            # 获取沪深 A 股列表
            df_sh = ak.stock_sh_a_spot_em()
            df_sz = ak.stock_sz_a_spot_em()
            
            stocks = []
            for df in [df_sh, df_sz]:
                for _, row in df.iterrows():
                    stocks.append({
                        'code': row.get('代码', ''),
                        'name': row.get('名称', ''),
                        'latest_price': float(row.get('最新价', 0)) if row.get('最新价') else None,
                        'change_percent': float(row.get('涨跌幅', 0)) if row.get('涨跌幅') else None,
                        'volume': float(row.get('成交量', 0)) if row.get('成交量') else None,
                        'turnover': float(row.get('成交额', 0)) if row.get('成交额') else None,
                        'market_cap': float(row.get('总市值', 0)) if row.get('总市值') else None,
                        'pe_ratio': float(row.get('市盈率 - 动态', 0)) if row.get('市盈率 - 动态') else None,
                        'pb_ratio': float(row.get('市净率', 0)) if row.get('市净率') else None,
                    })
            
            return stocks
        except Exception as e:
            print(f"AkShare 获取股票列表失败：{e}")
            return []
    
    def get_daily_data(self, code: str, start_date: str, end_date: str) -> List[Dict]:
        """
        获取日线数据
        
        Args:
            code: 股票代码 (600519)
            start_date: 开始日期 (20230101)
            end_date: 结束日期 (20231231)
        """
        try:
            # 判断市场
            if code.startswith('6'):
                market = "sh"
            else:
                market = "sz"
            
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
            
            daily_data = []
            for _, row in df.iterrows():
                daily_data.append({
                    'date': row.get('日期', ''),
                    'open': float(row.get('开盘', 0)) if row.get('开盘') else None,
                    'high': float(row.get('最高', 0)) if row.get('最高') else None,
                    'low': float(row.get('最低', 0)) if row.get('最低') else None,
                    'close': float(row.get('收盘', 0)) if row.get('收盘') else None,
                    'volume': float(row.get('成交量', 0)) if row.get('成交量') else None,
                    'turnover': float(row.get('成交额', 0)) if row.get('成交额') else None,
                })
            
            return daily_data
        except Exception as e:
            print(f"AkShare 获取日线数据失败 {code}: {e}")
            return []
    
    def get_realtime_quote(self, code: str) -> Optional[Dict]:
        """获取实时行情"""
        try:
            if code.startswith('6'):
                market = "sh"
            else:
                market = "sz"
            
            df = ak.stock_zh_a_spot_em()
            stock_data = df[df['代码'] == code]
            
            if len(stock_data) > 0:
                row = stock_data.iloc[0]
                return {
                    'code': code,
                    'name': row.get('名称', ''),
                    'price': float(row.get('最新价', 0)) if row.get('最新价') else None,
                    'change': float(row.get('涨跌额', 0)) if row.get('涨跌额') else None,
                    'change_percent': float(row.get('涨跌幅', 0)) if row.get('涨跌幅') else None,
                    'volume': float(row.get('成交量', 0)) if row.get('成交量') else None,
                    'turnover': float(row.get('成交额', 0)) if row.get('成交额') else None,
                    'high': float(row.get('最高', 0)) if row.get('最高') else None,
                    'low': float(row.get('最低', 0)) if row.get('最低') else None,
                    'open': float(row.get('今开', 0)) if row.get('今开') else None,
                    'prev_close': float(row.get('昨收', 0)) if row.get('昨收') else None,
                    'pe_ratio': float(row.get('市盈率 - 动态', 0)) if row.get('市盈率 - 动态') else None,
                    'pb_ratio': float(row.get('市净率', 0)) if row.get('市净率') else None,
                    'market_cap': float(row.get('总市值', 0)) if row.get('总市值') else None,
                }
            
            return None
        except Exception as e:
            print(f"AkShare 获取实时行情失败 {code}: {e}")
            return None
    
    def get_financials(self, code: str) -> Dict:
        """获取财务数据"""
        try:
            # 获取主要财务指标
            df = ak.stock_financial_analysis_indicator(symbol=code)
            
            if len(df) > 0:
                latest = df.iloc[0]
                return {
                    'code': code,
                    'report_date': latest.get('报告期', ''),
                    'roe': float(latest.get('净资产收益率 (%)', 0)) if latest.get('净资产收益率 (%)') else None,
                    'roa': float(latest.get('总资产净利润率 (%)', 0)) if latest.get('总资产净利润率 (%)') else None,
                    'gross_margin': float(latest.get('销售毛利率 (%)', 0)) if latest.get('销售毛利率 (%)') else None,
                    'net_margin': float(latest.get('销售净利率 (%)', 0)) if latest.get('销售净利率 (%)') else None,
                    'debt_ratio': float(latest.get('资产负债率 (%)', 0)) if latest.get('资产负债率 (%)') else None,
                }
            
            return {}
        except Exception as e:
            print(f"AkShare 获取财务数据失败 {code}: {e}")
            return {}


# 单例
akshare_service = AkShareService()
