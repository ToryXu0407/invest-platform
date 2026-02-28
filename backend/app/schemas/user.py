from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模式"""
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    """用户创建"""
    password: str = Field(..., min_length=6, description="密码至少 6 位")


class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """用户响应"""
    id: str
    role: str = "user"
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """用户更新"""
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
