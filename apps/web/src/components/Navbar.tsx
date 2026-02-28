'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV_ITEMS = [
  { href: '/', label: '首页', icon: '🏠' },
  { href: '/search', label: '选股', icon: '🔍' },
  { href: '/screener', label: '选股器', icon: '📊' },
  { href: '/articles', label: '文章', icon: '📚' },
  { href: '/ai', label: 'AI', icon: '🤖' },
  { href: '/alerts', label: '预警', icon: '🔔' },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link href="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">价值投资</span>
            </Link>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-1">
              {NAV_ITEMS.map(item => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    pathname === item.href
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              href="/login"
              className="text-gray-600 hover:text-gray-900 text-sm font-medium"
            >
              登录
            </Link>
            <Link
              href="/register"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
            >
              注册
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
