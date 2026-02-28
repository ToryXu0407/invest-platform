'use client';

import { useState } from 'react';
import { screenStocks, ScreenerRequest, ScreenerResult, PresetTemplate, getScreenerPresets } from '@/lib/api-screener';

const PRESETS: PresetTemplate[] = [
  {
    id: 'high_dividend',
    name: '高股息策略',
    description: '股息率 > 5%, PE < 20',
    conditions: { dividend_yield_min: 5, pe_max: 20 },
  },
  {
    id: 'low_valuation',
    name: '低估值策略',
    description: 'PE 百分位 < 20%, PB 百分位 < 20%',
    conditions: { pe_percentile_max: 20, pb_percentile_max: 20 },
  },
  {
    id: 'quality_growth',
    name: '优质成长策略',
    description: 'ROE > 15%, 营收增长率 > 20%',
    conditions: { roe_min: 15, revenue_growth_min: 20 },
  },
];

export default function ScreenerPage() {
  const [filters, setFilters] = useState<ScreenerRequest>({});
  const [results, setResults] = useState<ScreenerResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  async function handleScreen() {
    setLoading(true);
    try {
      const response = await screenStocks(filters);
      setResults(response.data || []);
    } catch (error) {
      console.error('选股失败:', error);
      alert('选股失败，请重试');
    } finally {
      setLoading(false);
    }
  }

  function applyPreset(preset: PresetTemplate) {
    setFilters(preset.conditions);
  }

  function handleExport() {
    const csv = [
      ['代码', '名称', '市场', '价格', 'PE', 'PB', '股息率', 'ROE'].join(','),
      ...results.map(r =>
        [r.code, r.name, r.market, r.current_price, r.pe_ttm, r.pb, r.dividend_yield, r.roe].join(',')
      ),
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `选股结果-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">选股器</h1>
          <p className="text-gray-600">多条件筛选，快速找到心仪标的</p>
        </div>

        {/* 预设模板 */}
        <div className="mb-6">
          <h2 className="text-lg font-bold mb-4">预设策略</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {PRESETS.map(preset => (
              <button
                key={preset.id}
                onClick={() => applyPreset(preset)}
                className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow text-left"
              >
                <div className="font-bold mb-1">{preset.name}</div>
                <div className="text-sm text-gray-600">{preset.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* 筛选条件 */}
        <div className="mb-6 bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold">筛选条件</h2>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="text-blue-600 hover:underline text-sm"
            >
              {showFilters ? '收起' : '展开高级选项'}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                PE 最大值
              </label>
              <input
                type="number"
                value={filters.pe_max || ''}
                onChange={(e) => setFilters({ ...filters, pe_max: parseFloat(e.target.value) || undefined })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="如：20"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                PB 最大值
              </label>
              <input
                type="number"
                value={filters.pb_max || ''}
                onChange={(e) => setFilters({ ...filters, pb_max: parseFloat(e.target.value) || undefined })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="如：5"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                股息率最小值 (%)
              </label>
              <input
                type="number"
                step="0.1"
                value={filters.dividend_yield_min || ''}
                onChange={(e) => setFilters({ ...filters, dividend_yield_min: parseFloat(e.target.value) || undefined })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="如：5"
              />
            </div>
          </div>

          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ROE 最小值 (%)
                </label>
                <input
                  type="number"
                  value={filters.roe_min || ''}
                  onChange={(e) => setFilters({ ...filters, roe_min: parseFloat(e.target.value) || undefined })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="如：15"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  营收增长率最小值 (%)
                </label>
                <input
                  type="number"
                  value={filters.revenue_growth_min || ''}
                  onChange={(e) => setFilters({ ...filters, revenue_growth_min: parseFloat(e.target.value) || undefined })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="如：20"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  市值范围 (亿)
                </label>
                <div className="flex gap-2">
                  <input
                    type="number"
                    value={filters.market_cap_min || ''}
                    onChange={(e) => setFilters({ ...filters, market_cap_min: parseFloat(e.target.value) || undefined })}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="最小"
                  />
                  <input
                    type="number"
                    value={filters.market_cap_max || ''}
                    onChange={(e) => setFilters({ ...filters, market_cap_max: parseFloat(e.target.value) || undefined })}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="最大"
                  />
                </div>
              </div>
            </div>
          )}

          <div className="mt-6 flex gap-4">
            <button
              onClick={handleScreen}
              disabled={loading}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? '筛选中...' : '开始筛选'}
            </button>
            <button
              onClick={() => setFilters({})}
              className="px-8 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              重置
            </button>
            {results.length > 0 && (
              <button
                onClick={handleExport}
                className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                导出 CSV
              </button>
            )}
          </div>
        </div>

        {/* 筛选结果 */}
        {loading && (
          <div className="text-center py-12 text-gray-500">筛选中...</div>
        )}

        {!loading && results.length > 0 && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
              <h2 className="text-lg font-bold">筛选结果 ({results.length})</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">代码</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">名称</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">市场</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">价格</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">PE</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">PB</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">股息率</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">ROE</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {results.map(stock => (
                    <tr key={stock.code} className="hover:bg-gray-50 cursor-pointer">
                      <td className="px-6 py-4 text-sm font-medium text-blue-600">{stock.code}</td>
                      <td className="px-6 py-4 text-sm font-medium">{stock.name}</td>
                      <td className="px-6 py-4 text-sm text-gray-500">{stock.market}</td>
                      <td className="px-6 py-4 text-sm text-right font-medium">¥{stock.current_price.toFixed(2)}</td>
                      <td className="px-6 py-4 text-sm text-right">{stock.pe_ttm?.toFixed(2) || '-'}</td>
                      <td className="px-6 py-4 text-sm text-right">{stock.pb?.toFixed(2) || '-'}</td>
                      <td className="px-6 py-4 text-sm text-right">{stock.dividend_yield?.toFixed(2) || '-'}%</td>
                      <td className="px-6 py-4 text-sm text-right">{stock.roe?.toFixed(2) || '-'}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {!loading && results.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-white rounded-lg shadow">
            暂无结果，请设置筛选条件后点击"开始筛选"
          </div>
        )}
      </div>
    </div>
  );
}
