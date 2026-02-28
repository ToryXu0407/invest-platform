'use client';

import { useEffect, useRef } from 'react';
import { createChart, IChartApi, ISeriesApi, CandlestickData } from 'lightweight-charts';

interface KLineChartProps {
  data: Array<{
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  }>;
}

export default function KLineChart({ data }: KLineChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candlestickSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return;

    // 创建图表
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { type: 'solid', color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      crosshair: {
        mode: 1, // MagnetMode
      },
      timeScale: {
        timeVisible: false,
        borderColor: '#ddd',
      },
      rightPriceScale: {
        borderColor: '#ddd',
      },
    });

    chartRef.current = chart;

    // 创建 K 线系列
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#ef4444', // 红色 - 涨
      downColor: '#22c55e', // 绿色 - 跌
      borderUpColor: '#ef4444',
      borderDownColor: '#22c55e',
      wickUpColor: '#ef4444',
      wickDownColor: '#22c55e',
    });

    candlestickSeriesRef.current = candlestickSeries;

    // 转换数据格式
    const candleData: CandlestickData[] = data.map((item) => ({
      time: item.date.replace(/-/g, '') as any,
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }));

    candlestickSeries.setData(candleData);

    // 自适应窗口大小
    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data]);

  if (data.length === 0) {
    return (
      <div className="bg-white rounded-lg p-12 text-center text-gray-500">
        暂无 K 线数据
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg p-4 shadow">
      <div ref={chartContainerRef} className="w-full" />
      <div className="mt-4 text-sm text-gray-500">
        <div className="flex items-center gap-4">
          <span className="flex items-center">
            <span className="w-3 h-3 bg-red-500 mr-2 rounded"></span>
            上涨
          </span>
          <span className="flex items-center">
            <span className="w-3 h-3 bg-green-500 mr-2 rounded"></span>
            下跌
          </span>
        </div>
      </div>
    </div>
  );
}
