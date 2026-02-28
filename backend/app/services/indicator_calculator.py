# 核心指标计算服务

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import statistics


class IndicatorCalculator:
    """核心指标计算器"""
    
    @staticmethod
    def calculate_dividend_yield(
        total_dividend: float,
        current_price: float
    ) -> Optional[float]:
        """
        计算股息率
        
        股息率 = 年度股息 / 当前股价 * 100%
        
        Args:
            total_dividend: 年度股息总和
            current_price: 当前股价
            
        Returns:
            股息率 (%)
        """
        if current_price <= 0:
            return None
        
        return (total_dividend / current_price) * 100
    
    @staticmethod
    def calculate_pe_ttm(
        market_cap: float,
        net_profits_last_4q: List[float]
    ) -> Optional[float]:
        """
        计算 PE-TTM
        
        PE-TTM = 总市值 / 最近 4 季度净利润总和
        
        Args:
            market_cap: 总市值
            net_profits_last_4q: 最近 4 季度净利润列表
            
        Returns:
            PE-TTM
        """
        if not net_profits_last_4q:
            return None
        
        total_profit = sum(net_profits_last_4q)
        
        if total_profit <= 0:
            return None  # 亏损无 PE
        
        return market_cap / total_profit
    
    @staticmethod
    def calculate_pb(
        market_cap: float,
        net_assets: float
    ) -> Optional[float]:
        """
        计算 PB
        
        PB = 总市值 / 最新净资产
        
        Args:
            market_cap: 总市值
            net_assets: 最新净资产
            
        Returns:
            PB
        """
        if net_assets <= 0:
            return None
        
        return market_cap / net_assets
    
    @staticmethod
    def calculate_true_money_index(
        operating_cash_flow: float,
        net_profit: float
    ) -> Optional[float]:
        """
        计算真钱指数
        
        真钱指数 = 经营现金流 / 归母净利润
        
        > 1.0: 利润质量高（真金白银）
        0.5-1.0: 利润质量一般
        < 0.5: 利润质量差（纸面富贵）
        
        Args:
            operating_cash_flow: 经营现金流
            net_profit: 归母净利润
            
        Returns:
            真钱指数
        """
        if net_profit == 0:
            return None
        
        return operating_cash_flow / net_profit
    
    @staticmethod
    def calculate_percentile(
        current_value: float,
        historical_data: List[float],
        days: int = 3650  # 默认 10 年
    ) -> Optional[float]:
        """
        计算百分位
        
        百分位 = (历史中小于当前值的数量 / 总数量) * 100
        
        Args:
            current_value: 当前值
            historical_data: 历史数据列表
            days: 统计天数
            
        Returns:
            百分位 (0-100)
        """
        if not historical_data or len(historical_data) == 0:
            return None
        
        # 过滤有效数据
        valid_data = [v for v in historical_data if v is not None and v > 0]
        
        if len(valid_data) == 0:
            return None
        
        count_lower = sum(1 for v in valid_data if v < current_value)
        percentile = (count_lower / len(valid_data)) * 100
        
        return round(percentile, 2)
    
    @staticmethod
    def get_valuation_status(percentile: float) -> str:
        """
        根据百分位判断估值状态
        
        Args:
            percentile: 百分位 (0-100)
            
        Returns:
            估值状态
        """
        if percentile is None:
            return "unknown"
        
        if percentile < 20:
            return "undervalued"  # 低估
        elif percentile < 50:
            return "low"  # 偏低
        elif percentile < 80:
            return "fair"  # 合理
        elif percentile < 90:
            return "high"  # 偏高
        else:
            return "overvalued"  # 高估
    
    @staticmethod
    def calculate_roe(
        net_profit: float,
        net_assets: float
    ) -> Optional[float]:
        """
        计算 ROE
        
        ROE = 净利润 / 净资产 * 100%
        
        Args:
            net_profit: 净利润
            net_assets: 净资产
            
        Returns:
            ROE (%)
        """
        if net_assets <= 0:
            return None
        
        return (net_profit / net_assets) * 100
    
    @staticmethod
    def calculate_growth_rate(
        current_value: float,
        previous_value: float
    ) -> Optional[float]:
        """
        计算增长率
        
        增长率 = (当前值 - 上期值) / 上期值 * 100%
        
        Args:
            current_value: 当前值
            previous_value: 上期值
            
        Returns:
            增长率 (%)
        """
        if previous_value <= 0:
            return None
        
        return ((current_value - previous_value) / previous_value) * 100
    
    @staticmethod
    def calculate_consecutive_dividend_years(
        dividends: List[Dict]
    ) -> int:
        """
        计算连续分红年数
        
        Args:
            dividends: 分红记录列表
            
        Returns:
            连续分红年数
        """
        if not dividends:
            return 0
        
        # 按年份排序
        years = set()
        for div in dividends:
            if div.get('ex_date'):
                year = div['ex_date'][:4]
                years.add(year)
        
        if not years:
            return 0
        
        # 检查连续性
        sorted_years = sorted(list(years), reverse=True)
        consecutive = 1
        
        for i in range(1, len(sorted_years)):
            if int(sorted_years[i-1]) - int(sorted_years[i]) == 1:
                consecutive += 1
            else:
                break
        
        return consecutive


# 单例
indicator_calculator = IndicatorCalculator()
