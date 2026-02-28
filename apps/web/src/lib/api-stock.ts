// 股票 API 服务
import apiClient from './api-client';

export interface Stock {
  id: string;
  code: string;
  name: string;
  market: string;
  industry?: string;
  latest_price?: number;
  change_percent?: number;
}

export interface StockIndicators {
  code: string;
  name: string;
  current_price: number;
  pe_ttm?: number;
  pb?: number;
  dividend_yield?: number;
  pe_percentile?: number;
  pb_percentile?: number;
  true_money_index?: number;
}

export interface DailyData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  pe_ttm?: number;
  pb?: number;
  dividend_yield?: number;
}

/**
 * 搜索股票
 */
export async function searchStocks(query: string, market?: string) {
  const params = new URLSearchParams({ q: query });
  if (market) params.append('market', market);
  
  return apiClient.get(`/api/v1/stocks?${params.toString()}`);
}

/**
 * 获取股票详情
 */
export async function getStockDetail(code: string) {
  return apiClient.get(`/api/v1/stocks/${code}`);
}

/**
 * 获取股票核心指标
 */
export async function getStockIndicators(code: string): Promise<StockIndicators> {
  return apiClient.get(`/api/v1/stocks/${code}/indicators`);
}

/**
 * 获取日线数据
 */
export async function getDailyData(
  code: string,
  startDate?: string,
  endDate?: string
) {
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  return apiClient.get(`/api/v1/stocks/${code}/daily?${params.toString()}`);
}

/**
 * 获取财务数据
 */
export async function getFinancials(code: string) {
  return apiClient.get(`/api/v1/stocks/${code}/financials`);
}
