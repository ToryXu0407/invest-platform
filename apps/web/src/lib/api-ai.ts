// AI 问答 API 服务
import apiClient from './api-client';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  history?: ChatMessage[];
}

export interface ChatResponse {
  message: string;
  sources?: string[];
  created_at: string;
}

export interface ChatHistory {
  id: string;
  message: string;
  response: string;
  created_at: string;
}

/**
 * AI 对话
 */
export async function chat(data: ChatRequest): Promise<ChatResponse> {
  return apiClient.post('/api/v1/ai/chat', data);
}

/**
 * 获取问答历史
 */
export async function getChatHistory(limit = 20): Promise<ChatHistory[]> {
  return apiClient.get(`/api/v1/ai/history?limit=${limit}`);
}

/**
 * 清空历史记录
 */
export async function clearChatHistory() {
  return apiClient.delete('/api/v1/ai/history');
}
