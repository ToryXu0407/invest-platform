# Celery 配置

from celery import Celery
from app.core.config import settings


# 创建 Celery 应用
celery_app = Celery(
    'invest_platform',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        'app.tasks.stock_tasks',
        'app.tasks.data_sync_tasks',
    ]
)

# Celery 配置
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 分钟超时
    worker_prefetch_multiplier=1,
)


# 定时任务配置
celery_app.conf.beat_schedule = {
    # 每天收盘后同步日线数据（A 股 15:30）
    'sync-daily-data': {
        'task': 'app.tasks.data_sync_tasks.sync_all_daily_data',
        'schedule': 0,  # 手动触发
    },
    
    # 每周一同步股票列表
    'sync-stock-list': {
        'task': 'app.tasks.data_sync_tasks.sync_stock_list_weekly',
        'schedule': 0,  # 手动触发
    },
    
    # 每天检查预警
    'check-alerts': {
        'task': 'app.tasks.alert_tasks.check_all_alerts',
        'schedule': 0,  # 手动触发
    },
}
