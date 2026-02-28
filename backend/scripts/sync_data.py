#!/usr/bin/env python3
"""
数据同步脚本

用法:
    python scripts/sync_data.py --stock 600519
    python scripts/sync_data.py --all
    python scripts/sync_data.py --init
"""

import asyncio
import argparse
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker, engine, Base
from app.services.stock_data_sync import StockDataSyncService
from app.services.data_sources.tushare_service import tushare_service


async def init_database():
    """初始化数据库（创建表）"""
    print("📊 初始化数据库...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 数据库表创建完成")


async def sync_stock_list():
    """同步股票列表"""
    print("📋 同步股票列表...")
    async with async_session_maker() as db:
        service = StockDataSyncService(db)
        count = await service.sync_stock_list()
    print(f"✅ 股票列表同步完成，共 {count} 只股票")


async def sync_single_stock(code: str):
    """同步单只股票数据"""
    print(f"📈 同步 {code} 数据...")
    async with async_session_maker() as db:
        service = StockDataSyncService(db)
        
        # 同步日线数据
        print("  └─ 同步日线数据...")
        daily_count = await service.sync_daily_data(code)
        print(f"     ✅ 日线数据：{daily_count} 条")
        
        # 同步财务数据
        print("  └─ 同步财务数据...")
        fina_count = await service.sync_financials(code)
        print(f"     ✅ 财务数据：{fina_count} 条")
    
    print(f"✅ {code} 同步完成")


async def sync_all_stocks():
    """同步所有股票数据"""
    print("📊 同步所有股票数据...")
    # TODO: 实现批量同步
    print("⚠️  该功能开发中，请先使用 --stock 参数同步单只股票")


async def main():
    parser = argparse.ArgumentParser(description='股票数据同步脚本')
    parser.add_argument('--stock', type=str, help='股票代码 (如：600519)')
    parser.add_argument('--all', action='store_true', help='同步所有股票')
    parser.add_argument('--init', action='store_true', help='初始化数据库')
    
    args = parser.parse_args()
    
    try:
        if args.init:
            await init_database()
            await sync_stock_list()
        
        if args.stock:
            await sync_single_stock(args.stock)
        
        if args.all:
            await sync_all_stocks()
        
        if not any([args.stock, args.all, args.init]):
            parser.print_help()
    
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
