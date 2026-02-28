'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getStockIndicators, getDailyData, StockIndicators, DailyData } from '@/lib/api-stock';
import KLineChart from '@/components/KLineChart';
import ValuationChart from '@/components/ValuationChart';
import IndicatorCard from '@/components/IndicatorCard';

export default function StockDetailPage() {
  const params = useParams();
  const code = params.code as string;
  
  const [indicators, setIndicators] = useState<StockIndicators | null>(null);
  const [dailyData, setDailyData] = useState<DailyData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError('');

      try {
        // 并行加载指标和日线数据
        const [indicatorsData, dailyDataResponse] = await Promise.all([
          getStockIndicators(code),
          getDailyData(code, '20240101', '20241231'),
        ]);

        setIndicators(indicatorsData);
        setDailyData(dailyDataResponse.data || []);
      } catch (err: any) {
        setError(err.message || '加载失败');
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [code]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">加载中...</div>
      </div>
    );
  }

  if (error || !indicators) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <div className="text-red-600 text-center py-12">
          {error || '加载失败'}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* 股票头部 */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">
          {indicators.code} - {indicators.name}
        </h1>
        <div className="text-4xl font-bold text-blue-600">
          ¥{indicators.current_price.toFixed(2)}
        </div>
      </div>

      {/* 核心指标卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <IndicatorCard
          title="股息率"
          value={indicators.dividend_yield}
          suffix="%"
          percentile={null}
          description="年度股息 / 当前股价"
        />
        <IndicatorCard
          title="PE-TTM"
          value={indicators.pe_ttm}
          percentile={indicators.pe_percentile}
          description="滚动市盈率"
        />
        <IndicatorCard
          title="PB"
          value={indicators.pb}
          percentile={indicators.pb_percentile}
          description="市净率"
        />
        <IndicatorCard
          title="真钱指数"
          value={indicators.true_money_index}
          percentile={null}
          description="经营现金流 / 净利润"
          formatValue={(v) => (v > 1 ? '优秀' : v > 0.5 ? '良好' : '较差')}
        />
      </div>

      {/* K 线图表 */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">K 线走势</h2>
        <KLineChart data={dailyData} />
      </div>

      {/* 估值图表 */}
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">估值分析</h2>
        <ValuationChart
          pe={indicators.pe_ttm}
          pb={indicators.pb}
          pePercentile={indicators.pe_percentile}
          pbPercentile={indicators.pb_percentile}
        />
      </div>
    </div>
  );
}
