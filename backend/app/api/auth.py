from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    auth_service = AuthService(db)
    user = await auth_service.register(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    auth_service = AuthService(db)
    tokens = await auth_service.authenticate(login_data.email, login_data.password)
    return tokens


@router.post("/logout")
async def logout():
    """用户登出"""
    # JWT 无状态，客户端删除 token 即可
    return {"message": "成功登出"}


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """刷新访问令牌"""
    # TODO: 实现刷新逻辑
    return {"access_token": "", "refresh_token": "", "token_type": "bearer"}
