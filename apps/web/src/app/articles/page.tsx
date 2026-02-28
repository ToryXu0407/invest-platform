'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getArticles, Article, ArticleFilters } from '@/lib/api-article';

const SERIES_OPTIONS = [
  { value: '', label: '全部' },
  { value: '天阶功法', label: '天阶功法（高级）' },
  { value: '地阶功法', label: '地阶功法（核心）' },
  { value: '玄阶功法', label: '玄阶功法（基础）' },
];

export default function ArticlesPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState<ArticleFilters>({
    series: '',
    page: 1,
    page_size: 20,
  });
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadArticles();
  }, [filters]);

  async function loadArticles() {
    setLoading(true);
    setError('');
    try {
      const response = await getArticles(filters);
      setArticles(response.data || []);
      setTotal(response.total || 0);
    } catch (err: any) {
      setError(err.message || '加载失败');
    } finally {
      setLoading(false);
    }
  }

  function handleSeriesChange(series: string) {
    setFilters(prev => ({ ...prev, series, page: 1 }));
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* 页面头部 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">投资知识库</h1>
          <p className="text-gray-600">
            收录 @MR Dang 知乎全部文章，支持时间线浏览、全文搜索
          </p>
        </div>

        {/* 筛选器 */}
        <div className="mb-6 flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">系列：</span>
            <div className="flex gap-2">
              {SERIES_OPTIONS.map(option => (
                <button
                  key={option.value}
                  onClick={() => handleSeriesChange(option.value)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filters.series === option.value
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
          <div className="ml-auto text-sm text-gray-600">
            共 {total} 篇文章
          </div>
        </div>

        {/* 加载状态 */}
        {loading && (
          <div className="text-center py-12">
            <div className="text-xl text-gray-500">加载中...</div>
          </div>
        )}

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* 文章列表 */}
        {!loading && !error && articles.length > 0 && (
          <div className="space-y-4">
            {articles.map(article => (
              <Link
                key={article.id}
                href={`/articles/${article.id}`}
                className="block bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h2 className="text-xl font-bold text-gray-900">
                        {article.title}
                      </h2>
                      {article.series && (
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                          {article.series}
                        </span>
                      )}
                    </div>
                    {article.summary && (
                      <p className="text-gray-600 mb-3 line-clamp-2">
                        {article.summary}
                      </p>
                    )}
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      {article.author && (
                        <span>作者：{article.author}</span>
                      )}
                      {article.published_at && (
                        <span>
                          发布：{new Date(article.published_at).toLocaleDateString('zh-CN')}
                        </span>
                      )}
                      {article.view_count !== undefined && (
                        <span>阅读：{article.view_count}</span>
                      )}
                    </div>
                  </div>
                  <div className="ml-4 text-gray-400">
                    <svg
                      className="w-6 h-6"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* 空状态 */}
        {!loading && !error && articles.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            暂无文章
          </div>
        )}

        {/* 分页 */}
        {!loading && !error && articles.length > 0 && (
          <div className="mt-8 flex justify-center gap-2">
            <button
              onClick={() => setFilters(prev => ({ ...prev, page: prev.page! - 1 }))}
              disabled={filters.page === 1}
              className="px-4 py-2 bg-white border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              上一页
            </button>
            <span className="px-4 py-2 text-gray-700">
              第 {filters.page} 页
            </span>
            <button
              onClick={() => setFilters(prev => ({ ...prev, page: prev.page! + 1 }))}
              disabled={articles.length < filters.page_size!}
              className="px-4 py-2 bg-white border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              下一页
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
