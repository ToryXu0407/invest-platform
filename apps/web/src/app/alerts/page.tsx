'use client';

import { useEffect, useState } from 'react';
import { getAlerts, createAlert, deleteAlert, Alert, CreateAlertRequest } from '@/lib/api-alert';

const ALERT_TYPES = [
  { value: 'dividend', label: '股息率' },
  { value: 'pe', label: 'PE' },
  { value: 'pb', label: 'PB' },
  { value: 'price', label: '价格' },
  { value: 'percentile', label: '百分位' },
];

const CONDITIONS = [
  { value: 'gt', label: '大于' },
  { value: 'lt', label: '小于' },
  { value: 'gte', label: '大于等于' },
  { value: 'lte', label: '小于等于' },
];

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState<CreateAlertRequest>({
    stock_code: '',
    alert_type: 'dividend',
    condition: 'gt',
    threshold: 0,
    notify_channel: 'wechat',
  });

  useEffect(() => {
    loadAlerts();
  }, []);

  async function loadAlerts() {
    try {
      const data = await getAlerts();
      setAlerts(data);
    } catch (error) {
      console.error('加载预警失败:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    try {
      await createAlert(formData);
      setShowCreateForm(false);
      loadAlerts();
      setFormData({
        stock_code: '',
        alert_type: 'dividend',
        condition: 'gt',
        threshold: 0,
        notify_channel: 'wechat',
      });
    } catch (error) {
      alert('创建失败');
    }
  }

  async function handleDelete(id: string) {
    if (!confirm('确定删除该预警？')) return;
    try {
      await deleteAlert(id);
      loadAlerts();
    } catch (error) {
      alert('删除失败');
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto p-6">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">价格预警</h1>
            <p className="text-gray-600">设置股票指标预警，支持微信/邮件推送</p>
          </div>
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            {showCreateForm ? '取消' : '+ 创建预警'}
          </button>
        </div>

        {/* 创建表单 */}
        {showCreateForm && (
          <div className="mb-8 bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">创建预警</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    股票代码
                  </label>
                  <input
                    type="text"
                    value={formData.stock_code}
                    onChange={(e) => setFormData({ ...formData, stock_code: e.target.value })}
                    required
                    placeholder="600519"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    预警类型
                  </label>
                  <select
                    value={formData.alert_type}
                    onChange={(e) => setFormData({ ...formData, alert_type: e.target.value as any })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    {ALERT_TYPES.map(type => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    条件
                  </label>
                  <select
                    value={formData.condition}
                    onChange={(e) => setFormData({ ...formData, condition: e.target.value as any })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    {CONDITIONS.map(cond => (
                      <option key={cond.value} value={cond.value}>{cond.label}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    阈值
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.threshold}
                    onChange={(e) => setFormData({ ...formData, threshold: parseFloat(e.target.value) })}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    通知渠道
                  </label>
                  <select
                    value={formData.notify_channel}
                    onChange={(e) => setFormData({ ...formData, notify_channel: e.target.value as any })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="wechat">微信</option>
                    <option value="email">邮件</option>
                    <option value="push">站内信</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-4">
                <button
                  type="submit"
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  创建
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  取消
                </button>
              </div>
            </form>
          </div>
        )}

        {/* 预警列表 */}
        {loading ? (
          <div className="text-center py-12 text-gray-500">加载中...</div>
        ) : alerts.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            暂无预警，点击右上角创建
          </div>
        ) : (
          <div className="space-y-4">
            {alerts.map(alert => (
              <div
                key={alert.id}
                className="bg-white rounded-lg shadow p-6 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-bold text-lg">{alert.stock_code}</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                      {ALERT_TYPES.find(t => t.value === alert.alert_type)?.label}
                    </span>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      alert.enabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                    }`}>
                      {alert.enabled ? '启用中' : '已禁用'}
                    </span>
                  </div>
                  <div className="text-gray-600 text-sm">
                    当 {alert.alert_type === 'dividend' ? '股息率' : alert.alert_type.toUpperCase()}{' '}
                    {CONDITIONS.find(c => c.value === alert.condition)?.label}{' '}
                    <span className="font-semibold">{alert.threshold}</span> 时触发
                  </div>
                  <div className="text-gray-500 text-xs mt-2">
                    通知渠道：{alert.notify_channel === 'wechat' ? '微信' : alert.notify_channel === 'email' ? '邮件' : '站内信'}
                    {alert.last_triggered && ` · 最后触发：${new Date(alert.last_triggered).toLocaleDateString('zh-CN')}`}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDelete(alert.id)}
                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    删除
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
