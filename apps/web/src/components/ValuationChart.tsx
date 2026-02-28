'use client';

import { useMemo } from 'react';

interface ValuationChartProps {
  pe?: number | null;
  pb?: number | null;
  pePercentile?: number | null;
  pbPercentile?: number | null;
}

export default function ValuationChart({
  pe,
  pb,
  pePercentile,
  pbPercentile,
}: ValuationChartProps) {
  // 获取估值状态和颜色
  const getValuationStatus = (percentile: number | null) => {
    if (percentile === null || percentile === undefined)
      return { text: '无数据', color: 'bg-gray-300' };
    if (percentile < 20) return { text: '低估', color: 'bg-green-500' };
    if (percentile < 50) return { text: '偏低', color: 'bg-green-300' };
    if (percentile < 80) return { text: '合理', color: 'bg-gray-400' };
    if (percentile < 90) return { text: '偏高', color: 'bg-red-300' };
    return { text: '高估', color: 'bg-red-500' };
  };

  const peStatus = useMemo(
    () => getValuationStatus(pePercentile),
    [pePercentile]
  );
  const pbStatus = useMemo(
    () => getValuationStatus(pbPercentile),
    [pbPercentile]
  );

  return (
    <div className="bg-white rounded-lg p-6 shadow">
      <h3 className="text-lg font-bold mb-6">估值状态分析</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* PE 百分位 */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">PE-TTM 百分位</span>
            <span className="text-sm text-gray-500">
              {pePercentile?.toFixed(1) || '-'}%
            </span>
          </div>
          <div className="relative h-8 bg-gray-200 rounded-full overflow-hidden">
            {/* 估值区间背景 */}
            <div className="absolute inset-0 flex">
              <div className="flex-1 bg-green-500" title="低估 (0-20%)" />
              <div className="flex-1 bg-green-300" title="偏低 (20-50%)" />
              <div className="flex-1 bg-gray-400" title="合理 (50-80%)" />
              <div className="flex-1 bg-red-300" title="偏高 (80-90%)" />
              <div className="flex-1 bg-red-500" title="高估 (90-100%)" />
            </div>
            {/* 当前值标记 */}
            {pePercentile !== null && pePercentile !== undefined && (
              <div
                className="absolute top-0 w-1 h-full bg-black opacity-50"
                style={{ left: `${pePercentile}%` }}
              />
            )}
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>0%</span>
            <span>20%</span>
            <span>50%</span>
            <span>80%</span>
            <span>90%</span>
            <span>100%</span>
          </div>
          <div className="mt-3 text-center">
            <span
              className={`inline-block px-3 py-1 rounded-full text-white text-sm ${peStatus.color}`}
            >
              PE 状态：{peStatus.text}
            </span>
          </div>
          {pe && (
            <div className="text-center mt-2 text-sm text-gray-600">
              当前 PE: {pe.toFixed(2)}
            </div>
          )}
        </div>

        {/* PB 百分位 */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">PB 百分位</span>
            <span className="text-sm text-gray-500">
              {pbPercentile?.toFixed(1) || '-'}%
            </span>
          </div>
          <div className="relative h-8 bg-gray-200 rounded-full overflow-hidden">
            {/* 估值区间背景 */}
            <div className="absolute inset-0 flex">
              <div className="flex-1 bg-green-500" title="低估 (0-20%)" />
              <div className="flex-1 bg-green-300" title="偏低 (20-50%)" />
              <div className="flex-1 bg-gray-400" title="合理 (50-80%)" />
              <div className="flex-1 bg-red-300" title="偏高 (80-90%)" />
              <div className="flex-1 bg-red-500" title="高估 (90-100%)" />
            </div>
            {/* 当前值标记 */}
            {pbPercentile !== null && pbPercentile !== undefined && (
              <div
                className="absolute top-0 w-1 h-full bg-black opacity-50"
                style={{ left: `${pbPercentile}%` }}
              />
            )}
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>0%</span>
            <span>20%</span>
            <span>50%</span>
            <span>80%</span>
            <span>90%</span>
            <span>100%</span>
          </div>
          <div className="mt-3 text-center">
            <span
              className={`inline-block px-3 py-1 rounded-full text-white text-sm ${pbStatus.color}`}
            >
              PB 状态：{pbStatus.text}
            </span>
          </div>
          {pb && (
            <div className="text-center mt-2 text-sm text-gray-600">
              当前 PB: {pb.toFixed(2)}
            </div>
          )}
        </div>
      </div>

      {/* 图例说明 */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h4 className="text-sm font-medium mb-3">估值区间说明</h4>
        <div className="grid grid-cols-5 gap-2 text-xs">
          <div className="text-center">
            <div className="w-full h-3 bg-green-500 rounded mb-1"></div>
            <div>低估</div>
            <div className="text-gray-500">0-20%</div>
          </div>
          <div className="text-center">
            <div className="w-full h-3 bg-green-300 rounded mb-1"></div>
            <div>偏低</div>
            <div className="text-gray-500">20-50%</div>
          </div>
          <div className="text-center">
            <div className="w-full h-3 bg-gray-400 rounded mb-1"></div>
            <div>合理</div>
            <div className="text-gray-500">50-80%</div>
          </div>
          <div className="text-center">
            <div className="w-full h-3 bg-red-300 rounded mb-1"></div>
            <div>偏高</div>
            <div className="text-gray-500">80-90%</div>
          </div>
          <div className="text-center">
            <div className="w-full h-3 bg-red-500 rounded mb-1"></div>
            <div>高估</div>
            <div className="text-gray-500">90-100%</div>
          </div>
        </div>
      </div>
    </div>
  );
}
