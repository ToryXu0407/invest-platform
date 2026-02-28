from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AlertBase(BaseModel):
    """预警基础模式"""
    stock_code: str = Field(..., description="股票代码")
    alert_type: str = Field(..., description="预警类型：dividend/pe/pb/price")
    threshold: Decimal = Field(..., description="阈值")
    condition: str = Field(..., description="条件：gt/lt/eq (大于/小于/等于)")


class AlertCreate(AlertBase):
    """预警创建"""
    notify_channel: str = Field(default="wechat", description="通知渠道：wechat/email")


class AlertResponse(AlertBase):
    """预警响应"""
    id: str
    user_id: str
    enabled: bool = True
    last_triggered: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    """预警更新"""
    threshold: Optional[Decimal] = None
    condition: Optional[str] = None
    enabled: Optional[bool] = None
    notify_channel: Optional[str] = None
