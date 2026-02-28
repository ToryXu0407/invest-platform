// 用户认证 API 服务
import apiClient from './api-client';

export interface User {
  id: string;
  email: string;
  name?: string;
  avatar_url?: string;
  phone?: string;
  role: string;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

/**
 * 用户注册
 */
export async function register(data: RegisterRequest): Promise<User> {
  return apiClient.post('/api/v1/auth/register', data);
}

/**
 * 用户登录
 */
export async function login(data: LoginRequest): Promise<TokenResponse> {
  const response = await apiClient.post('/api/v1/auth/login', data);
  // 保存 token
  if (response.access_token) {
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
  }
  return response;
}

/**
 * 用户登出
 */
export async function logout() {
  try {
    await apiClient.post('/api/v1/auth/logout');
  } finally {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
  }
}

/**
 * 获取当前用户信息
 */
export async function getCurrentUser(): Promise<User> {
  return apiClient.get('/api/v1/user/profile');
}

/**
 * 更新用户信息
 */
export async function updateProfile(data: Partial<User>) {
  return apiClient.put('/api/v1/user/profile', data);
}

/**
 * 刷新 Token
 */
export async function refreshToken(): Promise<TokenResponse> {
  const refresh_token = localStorage.getItem('refresh_token');
  if (!refresh_token) {
    throw new Error('No refresh token');
  }
  const response = await apiClient.post('/api/v1/auth/refresh', { refresh_token });
  if (response.access_token) {
    localStorage.setItem('token', response.access_token);
  }
  return response;
}
