import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '价值投资分析平台',
  description: '基于价值投资理念的股票分析平台 - 股息率锚定分析、财务数据可视化、AI 问答',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
        <footer className="bg-gray-900 text-white py-8 mt-16">
          <div className="max-w-7xl mx-auto px-4 text-center text-gray-400">
            <div className="mb-4">
              <span className="font-bold">价值投资分析平台</span> - 基于价值投资理念的股票分析工具
            </div>
            <div className="text-sm">
              © 2026 价值投资分析平台。仅供学习交流，不构成投资建议。
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}
