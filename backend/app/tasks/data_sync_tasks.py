# 数据同步定时任务

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from datetime import datetime, timedelta

from app.core.database import async_session_maker
from app.models.stock import Stock
from app.services.stock_data_sync import StockDataSyncService

logger = logging.getLogger(__name__)


@shared_task(name='tasks.data_sync_tasks.sync_stock_list_weekly')
def sync_stock_list_weekly():
    """
    每周同步股票列表
    每周一执行
    """
    logger.info("开始同步股票列表...")
    
    try:
        import asyncio
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    async def _sync():
        async with async_session_maker() as db:
            service = StockDataSyncService(db)
            count = await service.sync_stock_list()
            return count
    
    try:
        count = loop.run_until_complete(_sync())
        logger.info(f"股票列表同步完成，共 {count} 只股票")
    except Exception as e:
        logger.error(f"股票列表同步失败：{e}")


@shared_task(name='tasks.data_sync_tasks.sync_all_daily_data')
def sync_all_daily_data():
    """
    同步所有股票的日线数据
    每天收盘后执行
    """
    logger.info("开始同步所有股票日线数据...")
    
    try:
        import asyncio
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    async def _sync():
        async with async_session_maker() as db:
            # 获取所有股票
            result = await db.execute(select(Stock))
            stocks = result.scalars().all()
            
            sync_service = StockDataSyncService(db)
            total_count = 0
            success_count = 0
            
            for stock in stocks:
                try:
                    # 同步最近 30 天数据
                    end_date = datetime.now().strftime('%Y%m%d')
                    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
                    
                    count = await sync_service.sync_daily_data(
                        stock_code=stock.code,
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    total_count += count
                    if count > 0:
                        success_count += 1
                    
                    logger.info(f"同步 {stock.code} 完成，{count} 条数据")
                    
                except Exception as e:
                    logger.error(f"同步 {stock.code} 失败：{e}")
            
            return total_count, success_count
    
    try:
        total, success = loop.run_until_complete(_sync())
        logger.info(f"日线数据同步完成，总计 {total} 条，成功 {success} 只股票")
    except Exception as e:
        logger.error(f"日线数据同步失败：{e}")


@shared_task(name='tasks.data_sync_tasks.sync_single_stock')
def sync_single_stock(stock_code: str):
    """
    同步单只股票数据
    
    Args:
        stock_code: 股票代码
    """
    logger.info(f"开始同步 {stock_code} 数据...")
    
    try:
        import asyncio
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    async def _sync():
        async with async_session_maker() as db:
            service = StockDataSyncService(db)
            
            # 同步日线数据
            daily_count = await service.sync_daily_data(stock_code)
            
            # 同步财务数据
            fina_count = await service.sync_financials(stock_code)
            
            return daily_count, fina_count
    
    try:
        daily, fina = loop.run_until_complete(_sync())
        logger.info(f"{stock_code} 同步完成，日线{daily}条，财务{fina}条")
    except Exception as e:
        logger.error(f"{stock_code} 同步失败：{e}")


@shared_task(name='tasks.data_sync_tasks.sync_stock_financials')
def sync_stock_financials(stock_code: str):
    """
    同步单只股票财务数据
    
    Args:
        stock_code: 股票代码
    """
    logger.info(f"开始同步 {stock_code} 财务数据...")
    
    try:
        import asyncio
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    async def _sync():
        async with async_session_maker() as db:
            service = StockDataSyncService(db)
            count = await service.sync_financials(stock_code)
            return count
    
    try:
        count = loop.run_until_complete(_sync())
        logger.info(f"{stock_code} 财务数据同步完成，共{count}条")
    except Exception as e:
        logger.error(f"{stock_code} 财务数据同步失败：{e}")
