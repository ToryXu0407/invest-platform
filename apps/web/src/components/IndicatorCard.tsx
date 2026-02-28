import { useMemo } from 'react';

interface IndicatorCardProps {
  title: string;
  value?: number | null;
  suffix?: string;
  percentile?: number | null;
  description: string;
  formatValue?: (value: number) => string;
}

export default function IndicatorCard({
  title,
  value,
  suffix = '',
  percentile,
  description,
  formatValue,
}: IndicatorCardProps) {
  // 根据百分位计算颜色
  const getStatusColor = (p: number | null) => {
    if (p === null || p === undefined) return 'bg-gray-100';
    if (p < 20) return 'bg-green-100 border-green-500';
    if (p < 50) return 'bg-green-50 border-green-300';
    if (p < 80) return 'bg-gray-100';
    if (p < 90) return 'bg-red-50 border-red-300';
    return 'bg-red-100 border-red-500';
  };

  const getPercentileText = (p: number | null) => {
    if (p === null || p === undefined) return '';
    if (p < 20) return '低估';
    if (p < 50) return '偏低';
    if (p < 80) return '合理';
    if (p < 90) return '偏高';
    return '高估';
  };

  const displayValue = useMemo(() => {
    if (value === null || value === undefined) return '-';
    if (formatValue) return formatValue(value);
    return value.toFixed(2) + suffix;
  }, [value, suffix, formatValue]);

  return (
    <div
      className={`p-4 rounded-lg border-l-4 ${getStatusColor(percentile)} transition-all hover:shadow-md`}
    >
      <div className="text-sm text-gray-600 mb-1">{title}</div>
      <div className="text-2xl font-bold mb-2">{displayValue}</div>
      {percentile !== null && percentile !== undefined && (
        <div className="text-xs text-gray-500 mb-1">
          历史百分位：{percentile.toFixed(1)}% ({getPercentileText(percentile)})
        </div>
      )}
      <div className="text-xs text-gray-400">{description}</div>
    </div>
  );
}
