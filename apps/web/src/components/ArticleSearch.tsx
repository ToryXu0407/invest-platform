'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { searchArticles } from '@/lib/api-article';

export default function ArticleSearch() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await searchArticles(query);
      setResults(response.data || []);
    } catch (error) {
      console.error('搜索失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-8">
      <form onSubmit={handleSearch} className="flex gap-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索文章内容..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? '搜索中...' : '搜索'}
        </button>
      </form>
      {results.length > 0 && (
        <div className="mt-4 bg-white rounded-lg shadow p-4">
          <h3 className="font-bold mb-2">搜索结果</h3>
          <ul className="space-y-2">
            {results.map((article) => (
              <li
                key={article.id}
                onClick={() => router.push(`/articles/${article.id}`)}
                className="cursor-pointer hover:bg-gray-50 p-2 rounded"
              >
                <div className="font-medium">{article.title}</div>
                <div className="text-sm text-gray-600">{article.summary}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
