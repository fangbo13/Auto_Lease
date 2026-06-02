import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Loader2, Download, RefreshCw } from 'lucide-react'
import { getLeaseInput, triggerCalculation } from '../api/leaseInputs'
import { exportWorkingPaper } from '../api/export'
import { useAppStore } from '../store/appStore'
import { LeaseInput, CalculationResult as CalcResultType, AmortizationScheduleItem } from '../types'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

export default function CalculationResult() {
  const { id } = useParams<{ id: string }>()
  const [loading, setLoading] = useState(true)
  const [calculating, setCalculating] = useState(false)
  const [exporting, setExporting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [leaseInput, setLeaseInput] = useState<LeaseInput | null>(null)
  const [result, setResult] = useState<CalcResultType | null>(null)
  const [schedule, setSchedule] = useState<AmortizationScheduleItem[]>([])

  const fetchData = async () => {
    if (!id) return
    setLoading(true)
    try {
      const li = await getLeaseInput(id)
      setLeaseInput(li)
      const calcData = await triggerCalculation(id)
      setResult(calcData)
      // Fetch schedule via API (simplified: using the calculation response)
      // In real app, we'd fetch /api/calculate/results/{id}/schedule/
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [id])

  const handleExport = async () => {
    if (!id) return
    setExporting(true)
    try {
      const blob = await exportWorkingPaper(id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `租赁审计底稿_${leaseInput?.lease_name || '未命名'}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setExporting(false)
    }
  }

  const handleRecalculate = async () => {
    if (!id) return
    setCalculating(true)
    try {
      const calcData = await triggerCalculation(id)
      setResult(calcData)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setCalculating(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
        <span className="ml-3 text-gray-600">加载中...</span>
      </div>
    )
  }

  if (error || !result) {
    return (
      <div className="card text-center py-12">
        <p className="text-red-600 mb-4">{error || '计算结果未找到'}</p>
        <button onClick={fetchData} className="btn-primary">重试</button>
      </div>
    )
  }

  const chartData = schedule.map((s) => ({
    period: `第${s.period_number}期`,
    负债余额: Number(s.closing_liability),
    使用权资产净值: Number(s.rou_asset_closing),
  }))

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{leaseInput?.lease_name}</h1>
          <p className="text-sm text-gray-500 mt-1">
            开始日: {leaseInput?.lease_commencement_date} · 期限: {leaseInput?.lease_term_months} 个月
          </p>
        </div>
        <div className="flex space-x-3">
          <button onClick={handleRecalculate} disabled={calculating} className="btn-secondary flex items-center disabled:opacity-50">
            <RefreshCw className={`w-4 h-4 mr-2 ${calculating ? 'animate-spin' : ''}`} />
            重新计算
          </button>
          <button onClick={handleExport} disabled={exporting} className="btn-primary flex items-center disabled:opacity-50">
            <Download className="w-4 h-4 mr-2" />
            {exporting ? '导出中...' : '下载审计底稿'}
          </button>
        </div>
      </div>

      {/* Key metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard label="使用权资产" value={result.right_of_use_asset} />
        <MetricCard label="租赁负债" value={result.lease_liability} />
        <MetricCard label="总利息费用" value={result.total_interest} />
        <MetricCard label="总折旧费用" value={result.total_depreciation} />
      </div>

      {/* Chart */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">负债与使用权资产趋势</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData.length > 0 ? chartData : []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis />
              <Tooltip formatter={(value: number) => value.toFixed(2)} />
              <Legend />
              <Area type="monotone" dataKey="负债余额" stroke="#2563eb" fill="#3b82f6" fillOpacity={0.3} />
              <Area type="monotone" dataKey="使用权资产净值" stroke="#16a34a" fill="#22c55e" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Schedule table */}
      <div className="card overflow-x-auto">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">摊销明细表</h3>
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-3 py-2 text-left font-medium text-gray-600">期次</th>
              <th className="px-3 py-2 text-left font-medium text-gray-600">日期</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">期初负债</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">付款额</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">利息</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">本金</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">期末负债</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">折旧</th>
              <th className="px-3 py-2 text-right font-medium text-gray-600">ROU净值</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {schedule.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-3 py-2">{item.period_number}</td>
                <td className="px-3 py-2">{item.period_start_date}</td>
                <td className="px-3 py-2 text-right">{Number(item.opening_liability).toFixed(2)}</td>
                <td className="px-3 py-2 text-right">{Number(item.payment_amount).toFixed(2)}</td>
                <td className="px-3 py-2 text-right">{Number(item.interest_expense).toFixed(2)}</td>
                <td className="px-3 py-2 text-right">{Number(item.principal_reduction).toFixed(2)}</td>
                <td className="px-3 py-2 text-right">{Number(item.closing_liability).toFixed(2)}</td>
                <td className="px-3 py-2 text-right">{Number(item.depreciation_expense).toFixed(2)}</td>
                <td className="px-3 py-2 text-right">{Number(item.rou_asset_closing).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function MetricCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="card p-4">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-900 mt-1">
        {Number(value).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
      </p>
    </div>
  )
}
