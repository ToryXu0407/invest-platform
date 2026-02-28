// 选股器 API 服务
import apiClient from './api-client';

export interface ScreenerRequest {
  // 估值指标
  pe_min?: number;
  pe_max?: number;
  pb_min?: number;
  pb_max?: number;
  pe_percentile_max?: number;
  pb_percentile_max?: number;
  
  // 股息率
  dividend_yield_min?: number;
  
  // 财务指标
  roe_min?: number;
  revenue_growth_min?: number;
  profit_growth_min?: number;
  
  // 市值
  market_cap_min?: number;
  market_cap_max?: number;
  
  // 市场
  markets?: string[];
  
  // 行业
  industries?: string[];
}

export interface ScreenerResult {
  code: string;
  name: string;
  market: string;
  industry?: string;
  current_price: number;
  pe_ttm?: number;
  pb?: number;
  dividend_yield?: number;
  roe?: number;
}

export interface ScreenerResponse {
  data: ScreenerResult[];
  total: number;
  conditions: Record<string, any>;
}

export interface PresetTemplate {
  id: string;
  name: string;
  description: string;
  conditions: Partial<ScreenerRequest>;
}

/**
 * 选股器筛选
 */
export async function screenStocks(data: ScreenerRequest): Promise<ScreenerResponse> {
  return apiClient.post('/api/v1/screener', data);
}

/**
 * 获取预设模板
 */
export async function getScreenerPresets(): Promise<{ presets: PresetTemplate[] }> {
  return apiClient.get('/api/v1/screener/presets');
}

/**
 * 应用预设模板
 */
export async function applyPreset(presetId: string): Promise<Partial<ScreenerRequest>> {
  const response = await getScreenerPresets();
  const preset = response.presets.find(p => p.id === presetId);
  if (!preset) {
    throw new Error('Preset not found');
  }
  return preset.conditions;
}
