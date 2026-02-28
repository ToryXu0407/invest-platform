import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-6 text-gray-900">
            价值投资分析平台
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            基于价值投资理念的股票分析平台 - 股息率锚定分析、财务数据可视化、AI 问答
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/search"
              className="px-8 py-4 bg-blue-600 text-white rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors shadow-lg"
            >
              开始搜索股票
            </Link>
            <Link
              href="/docs"
              className="px-8 py-4 bg-white text-blue-600 border-2 border-blue-600 rounded-lg text-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              查看文档
            </Link>
          </div>
        </div>

        {/* 核心功能 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">股票分析</h3>
            <p className="text-gray-600">
              股息率锚定、PE/PB 百分位、真钱指数等核心指标分析
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-xl font-bold mb-2">K 线图表</h3>
            <p className="text-gray-600">
              交互式 K 线图，支持多周期切换和技术指标叠加
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold mb-2">AI 问答</h3>
            <p className="text-gray-600">
              基于 RAG 的智能问答，熟读投资经典，解答投资问题
            </p>
          </div>
        </div>

        {/* 热门股票示例 */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-bold mb-6">热门股票示例</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              href="/stocks/600519"
              className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="font-bold text-lg">600519</div>
              <div className="text-gray-600">贵州茅台</div>
              <div className="text-sm text-gray-500 mt-2">白酒行业龙头</div>
            </Link>
            <Link
              href="/stocks/000858"
              className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="font-bold text-lg">000858</div>
              <div className="text-gray-600">五粮液</div>
              <div className="text-sm text-gray-500 mt-2">浓香型白酒代表</div>
            </Link>
            <Link
              href="/stocks/601318"
              className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="font-bold text-lg">601318</div>
              <div className="text-gray-600">中国平安</div>
              <div className="text-sm text-gray-500 mt-2">保险行业龙头</div>
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-20">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-bold mb-4">关于平台</h3>
              <p className="text-gray-400">
                基于价值投资理念的股票分析工具，帮助投资者进行理性投资决策。
              </p>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">核心功能</h3>
              <ul className="text-gray-400 space-y-2">
                <li>• 股票基本面分析</li>
                <li>• 估值百分位计算</li>
                <li>• 财务数据可视化</li>
                <li>• AI 智能问答</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-4">免责声明</h3>
              <p className="text-gray-400">
                本平台仅供参考学习，不构成投资建议。投资有风险，入市需谨慎。
              </p>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            © 2026 价值投资分析平台。仅供学习交流使用。
          </div>
        </div>
      </footer>
    </main>
  );
}
