# Placeholder for article service
class ArticleService:
    """文章服务"""
    
    def __init__(self, db):
        self.db = db
    
    async def list_articles(self, search=None, series=None, page=1, page_size=20):
        """获取文章列表"""
        # TODO: 实现
        return [], 0
    
    async def get_article(self, article_id):
        """获取文章详情"""
        # TODO: 实现
        return None
    
    async def search_articles(self, query, page=1, page_size=20):
        """搜索文章"""
        # TODO: 实现 Elasticsearch/Meilisearch 集成
        return []
