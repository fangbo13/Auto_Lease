import { Link } from 'react-router-dom'
import { Upload, FileText, Download, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          租赁使用权资产自动计算
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          基于 IFRS 16 / ASC 842 准则，自动识别租赁合同、计算使用权资产与租赁负债，
          生成完整审计底稿。
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/upload" className="card hover:shadow-md transition-shadow group">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-primary-50 rounded-lg group-hover:bg-primary-100 transition-colors">
              <Upload className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">上传合同</h3>
              <p className="text-sm text-gray-500 mt-1">AI 自动识别合同关键信息</p>
            </div>
          </div>
        </Link>

        <Link to="/manual" className="card hover:shadow-md transition-shadow group">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-green-50 rounded-lg group-hover:bg-green-100 transition-colors">
              <FileText className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">手动填写</h3>
              <p className="text-sm text-gray-500 mt-1">多步骤表单输入租赁参数</p>
            </div>
          </div>
        </Link>

        <div className="card">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-purple-50 rounded-lg">
              <Download className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">导出底稿</h3>
              <p className="text-sm text-gray-500 mt-1">中国式审计风格 Excel</p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="w-5 h-5 text-primary-600" />
          <h2 className="text-lg font-semibold text-gray-900">功能特点</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
          <ul className="space-y-2">
            <li className="flex items-start">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-1.5 mr-2 flex-shrink-0" />
              支持 PDF、PNG、JPG 格式合同上传与 AI 解析
            </li>
            <li className="flex items-start">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-1.5 mr-2 flex-shrink-0" />
              GPT-4 Vision / Qwen / Tesseract 多解析器可插拔
            </li>
            <li className="flex items-start">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-1.5 mr-2 flex-shrink-0" />
              严格遵循 IFRS 16 / ASC 842 准则计算
            </li>
          </ul>
          <ul className="space-y-2">
            <li className="flex items-start">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-1.5 mr-2 flex-shrink-0" />
              支持月付、季付、年付及期初/期末付款
            </li>
            <li className="flex items-start">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-1.5 mr-2 flex-shrink-0" />
              生成完整摊销明细表与可视化图表
            </li>
            <li className="flex items-start">
              <span className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-1.5 mr-2 flex-shrink-0" />
              中国式审计底稿 Excel 一键导出
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
