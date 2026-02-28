'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { searchStocks, Stock } from '@/lib/api-stock';

export default function StockSearch() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');

    try {
      const data = await searchStocks(query);
      setResults(data.data || []);
    } catch (err: any) {
      setError(err.message || '搜索失败');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleStockClick = (code: string) => {
    router.push(`/stocks/${code}`);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">股票搜索</h1>

      <form onSubmit={handleSearch} className="mb-8">
        <div className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="输入股票代码或名称（如：600519 或 贵州茅台）"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>
      </form>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {results.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold">
              搜索结果 ({results.length})
            </h2>
          </div>
          <ul className="divide-y divide-gray-200">
            {results.map((stock) => (
              <li
                key={stock.id}
                onClick={() => handleStockClick(stock.code)}
                className="px-6 py-4 hover:bg-gray-50 cursor-pointer transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-3">
                      <span className="font-semibold text-lg">
                        {stock.code}
                      </span>
                      <span className="text-xl font-bold">{stock.name}</span>
                    </div>
                    <div className="text-sm text-gray-500 mt-1">
                      {stock.market}
                      {stock.industry && ` · ${stock.industry}`}
                    </div>
                  </div>
                  {stock.latest_price !== undefined && (
                    <div className="text-right">
                      <div className="text-lg font-semibold">
                        ¥{stock.latest_price.toFixed(2)}
                      </div>
                      <div
                        className={`text-sm ${
                          stock.change_percent >= 0
                            ? 'text-red-600'
                            : 'text-green-600'
                        }`}
                      >
                        {stock.change_percent >= 0 ? '+' : ''}
                        {stock.change_percent.toFixed(2)}%
                      </div>
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {results.length === 0 && query && !loading && !error && (
        <div className="text-center py-12 text-gray-500">
          未找到相关股票，请尝试其他关键词
        </div>
      )}
    </div>
  );
}
