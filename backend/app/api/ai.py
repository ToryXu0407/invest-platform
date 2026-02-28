from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.ai import ChatRequest, ChatResponse, ChatHistory
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """AI 智能问答"""
    ai_service = AIService(db)
    response = await ai_service.chat(current_user.id, request.message, request.history)
    return response


@router.get("/history", response_model=List[ChatHistory])
async def get_chat_history(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    """获取问答历史"""
    ai_service = AIService(db)
    history = await ai_service.get_history(current_user.id, limit)
    return history
