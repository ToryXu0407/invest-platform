// 文章 API 服务
import apiClient from './api-client';

export interface Article {
  id: string;
  title: string;
  content: string;
  summary?: string;
  author?: string;
  source_url?: string;
  series?: string;  // 天阶功法/地阶功法/玄阶功法
  published_at?: string;
  view_count?: number;
  created_at: string;
  updated_at: string;
}

export interface ArticleListResponse {
  data: Article[];
  total: number;
  page: number;
  page_size: number;
}

export interface ArticleFilters {
  q?: string;        // 搜索关键词
  series?: string;   // 系列分类
  page?: number;
  page_size?: number;
}

/**
 * 获取文章列表
 */
export async function getArticles(filters?: ArticleFilters): Promise<ArticleListResponse> {
  const params = new URLSearchParams();
  if (filters?.q) params.append('q', filters.q);
  if (filters?.series) params.append('series', filters.series);
  if (filters?.page) params.append('page', filters.page.toString());
  if (filters?.page_size) params.append('page_size', filters.page_size.toString());
  
  return apiClient.get(`/api/v1/articles?${params.toString()}`);
}

/**
 * 获取文章详情
 */
export async function getArticle(id: string): Promise<Article> {
  return apiClient.get(`/api/v1/articles/${id}`);
}

/**
 * 搜索文章
 */
export async function searchArticles(query: string, page = 1, page_size = 20) {
  return apiClient.get(`/api/v1/articles/search?q=${query}&page=${page}&page_size=${page_size}`);
}

/**
 * 更新阅读状态
 */
export async function updateReadingStatus(articleId: string, status: 'todo' | 'reading' | 'read' | 'bookmarked') {
  return apiClient.post(`/api/v1/articles/${articleId}/reading-status`, { status });
}

/**
 * 获取阅读状态
 */
export async function getReadingStatus(articleId: string) {
  return apiClient.get(`/api/v1/articles/${articleId}/reading-status`);
}

/**
 * 批量获取阅读状态
 */
export async function getReadingStatuses(articleIds: string[]) {
  return apiClient.post('/api/v1/articles/reading-statuses/batch', { article_ids: articleIds });
}
