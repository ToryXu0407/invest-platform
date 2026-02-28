import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserAlert(Base):
    """用户预警模型"""
    __tablename__ = "user_alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    stock_id = Column(String, ForeignKey("stocks.id"), nullable=False)
    alert_type = Column(String, nullable=False)  # dividend/pe/pb/price
    condition = Column(String, nullable=False)  # gt/lt/eq
    threshold = Column(Numeric(12, 4), nullable=False)
    enabled = Column(Boolean, default=True)
    notify_channel = Column(String)  # wechat/email
    last_triggered = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User")
    stock = relationship("Stock")
    
    def __repr__(self):
        return f"<UserAlert {self.user_id} {self.alert_type}>"
