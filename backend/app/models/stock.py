import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Numeric, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Stock(Base):
    """股票基础信息模型"""
    __tablename__ = "stocks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    market = Column(String, nullable=False)  # A 股/港股/美股
    industry = Column(String)
    sector = Column(String)
    listed_date = Column(Date)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    daily_data = relationship("StockDailyData", back_populates="stock")
    financials = relationship("StockFinancial", back_populates="stock")
    
    def __repr__(self):
        return f"<Stock {self.code} - {self.name}>"


class StockDailyData(Base):
    """股票日线数据模型"""
    __tablename__ = "stock_daily_data"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stock_id = Column(String, ForeignKey("stocks.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    open = Column(Numeric(12, 4))
    high = Column(Numeric(12, 4))
    low = Column(Numeric(12, 4))
    close = Column(Numeric(12, 4))
    volume = Column(Numeric)
    amount = Column(Numeric(20, 4))
    pe_ttm = Column(Numeric(12, 4))
    pb = Column(Numeric(12, 4))
    dividend_yield = Column(Numeric(8, 4))
    
    stock = relationship("Stock", back_populates="daily_data")
    
    __table_args__ = (
        UniqueConstraint('stock_id', 'date', name='uq_stock_date'),
    )
    
    def __repr__(self):
        return f"<StockDailyData {self.stock_id} {self.date}>"


class StockFinancial(Base):
    """股票财务数据模型"""
    __tablename__ = "stock_financials"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stock_id = Column(String, ForeignKey("stocks.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    report_type = Column(String)  # 年报/季报
    revenue = Column(Numeric(20, 4))
    net_profit = Column(Numeric(20, 4))
    operating_cash_flow = Column(Numeric(20, 4))
    total_assets = Column(Numeric(20, 4))
    total_liabilities = Column(Numeric(20, 4))
    equity = Column(Numeric(20, 4))
    roe = Column(Numeric(8, 4))
    
    stock = relationship("Stock", back_populates="financials")
    
    __table_args__ = (
        UniqueConstraint('stock_id', 'report_date', 'report_type', name='uq_stock_report'),
    )
    
    def __repr__(self):
        return f"<StockFinancial {self.stock_id} {self.report_date}>"
