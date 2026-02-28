'use client';

import { useState, useRef, useEffect } from 'react';
import { chat, getChatHistory, ChatMessage, ChatHistory } from '@/lib/api-ai';

export default function AIChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<ChatHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function loadHistory() {
    try {
      const data = await getChatHistory(20);
      setHistory(data);
    } catch (error) {
      console.error('加载历史失败:', error);
    }
  }

  async function handleSend() {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chat({ message: input, history: messages });
      const assistantMessage: ChatMessage = { role: 'assistant', content: response.message };
      setMessages(prev => [...prev, assistantMessage]);
      
      // 刷新历史
      loadHistory();
    } catch (error) {
      console.error('对话失败:', error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: '抱歉，出现错误，请稍后重试' },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyPress(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function loadChatSession(session: ChatHistory) {
    setMessages([
      { role: 'user', content: session.message },
      { role: 'assistant', content: session.response },
    ]);
    setShowHistory(false);
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* 侧边栏 - 历史记录 */}
      {showHistory && (
        <div className="w-80 bg-white border-r border-gray-200 p-4 overflow-y-auto">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold">问答历史</h2>
            <button
              onClick={() => setShowHistory(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
          {history.length === 0 ? (
            <div className="text-gray-500 text-sm text-center py-8">暂无历史记录</div>
          ) : (
            <div className="space-y-2">
              {history.map(item => (
                <button
                  key={item.id}
                  onClick={() => loadChatSession(item)}
                  className="w-full text-left p-3 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="text-sm font-medium truncate">{item.message}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(item.created_at).toLocaleDateString('zh-CN')}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {/* 主聊天区域 */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full">
        {/* 头部 */}
        <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">AI 投资助手</h1>
            <p className="text-sm text-gray-600">基于 RAG 的智能问答，熟读投资经典</p>
          </div>
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
          >
            📜 历史记录
          </button>
        </div>

        {/* 消息列表 */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <div className="text-6xl mb-4">🤖</div>
              <div className="text-xl font-bold mb-2">你好！我是 AI 投资助手</div>
              <div className="text-gray-600">
                我可以回答投资相关问题，比如：
                <div className="mt-4 space-y-2 text-left inline-block">
                  <div className="bg-gray-100 px-4 py-2 rounded-lg">• 如何判断股票估值高低？</div>
                  <div className="bg-gray-100 px-4 py-2 rounded-lg">• 股息率锚定法是什么？</div>
                  <div className="bg-gray-100 px-4 py-2 rounded-lg">• 贵州茅台现在值得买入吗？</div>
                </div>
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-gray-200'
                    }`}
                  >
                    <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* 输入框 */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="flex gap-4">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="输入你的问题..."
              rows={3}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed self-end"
            >
              发送
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500 text-center">
            AI 回答仅供参考，不构成投资建议
          </div>
        </div>
      </div>
    </div>
  );
}
