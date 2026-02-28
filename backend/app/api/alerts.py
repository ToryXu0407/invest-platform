from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.schemas.user import UserResponse
from app.services.alert_service import AlertService

router = APIRouter()


@router.get("", response_model=List[AlertResponse])
async def get_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取用户的预警列表"""
    alert_service = AlertService(db)
    alerts = await alert_service.get_user_alerts(current_user.id)
    return alerts


@router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(
    alert_data: AlertCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """创建价格预警"""
    alert_service = AlertService(db)
    alert = await alert_service.create_alert(current_user.id, alert_data)
    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: str,
    alert_data: AlertUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """更新预警"""
    alert_service = AlertService(db)
    alert = await alert_service.update_alert(current_user.id, alert_id, alert_data)
    if not alert:
        raise HTTPException(status_code=404, detail="预警不存在")
    return alert


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """删除预警"""
    alert_service = AlertService(db)
    success = await alert_service.delete_alert(current_user.id, alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="预警不存在")
    return {"message": "预警已删除"}
