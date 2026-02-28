# Placeholder for AI service
class AIService:
    """AI 问答服务"""
    
    def __init__(self, db):
        self.db = db
    
    async def chat(self, user_id, message, history=None):
        """AI 对话"""
        # TODO: 实现 LangChain/LlamaIndex RAG
        return {
            "message": "AI 服务正在开发中...",
            "sources": [],
        }
    
    async def get_history(self, user_id, limit=20):
        """获取问答历史"""
        # TODO: 实现
        return []
