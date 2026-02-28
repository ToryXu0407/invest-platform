// 价格预警 API 服务
import apiClient from './api-client';

export interface Alert {
  id: string;
  user_id: string;
  stock_code: string;
  stock_name?: string;
  alert_type: 'dividend' | 'pe' | 'pb' | 'price' | 'percentile';
  condition: 'gt' | 'lt' | 'eq' | 'gte' | 'lte';
  threshold: number;
  enabled: boolean;
  notify_channel: 'wechat' | 'email' | 'push';
  last_triggered?: string;
  created_at: string;
}

export interface CreateAlertRequest {
  stock_code: string;
  alert_type: Alert['alert_type'];
  condition: Alert['condition'];
  threshold: number;
  notify_channel?: Alert['notify_channel'];
}

export interface UpdateAlertRequest {
  threshold?: number;
  condition?: Alert['condition'];
  enabled?: boolean;
  notify_channel?: Alert['notify_channel'];
}

/**
 * 获取预警列表
 */
export async function getAlerts(): Promise<Alert[]> {
  return apiClient.get('/api/v1/alerts');
}

/**
 * 创建预警
 */
export async function createAlert(data: CreateAlertRequest): Promise<Alert> {
  return apiClient.post('/api/v1/alerts', data);
}

/**
 * 更新预警
 */
export async function updateAlert(id: string, data: UpdateAlertRequest): Promise<Alert> {
  return apiClient.put(`/api/v1/alerts/${id}`, data);
}

/**
 * 删除预警
 */
export async function deleteAlert(id: string) {
  return apiClient.delete(`/api/v1/alerts/${id}`);
}

/**
 * 测试预警
 */
export async function testAlert(id: string) {
  return apiClient.post(`/api/v1/alerts/${id}/test`);
}
