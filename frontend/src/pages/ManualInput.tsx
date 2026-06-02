import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronRight, ChevronLeft, Check } from 'lucide-react'
import { createLeaseInput } from '../api/leaseInputs'
import { useAppStore } from '../store/appStore'

const STEPS = ['基本信息', '付款条件', '利率与费用', '确认提交']

export default function ManualInput() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const setCurrentLeaseInput = useAppStore((s) => s.setCurrentLeaseInput)

  const [formData, setFormData] = useState({
    lease_name: '',
    lease_commencement_date: '',
    lease_term_months: 12,
    standard: 'IFRS16' as const,
    payment_frequency: 'monthly' as const,
    payment_amount: '',
    payment_timing: 'end' as const,
    discount_rate: '0.05',
    discount_rate_type: 'incremental_borrowing' as const,
    tax_rate: '0',
    initial_direct_costs: '0',
    lease_incentives: '0',
    residual_value_guarantee: '0',
    purchase_option: false,
    purchase_option_price: '',
    notes: '',
  })

  const updateField = (field: string, value: unknown) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const validateStep = () => {
    setError(null)
    if (step === 0) {
      if (!formData.lease_name) return setError('请输入租赁名称')
      if (!formData.lease_commencement_date) return setError('请选择租赁开始日')
      if (!formData.lease_term_months || formData.lease_term_months < 1) return setError('请输入有效的租赁期限')
    }
    if (step === 1) {
      if (!formData.payment_amount || Number(formData.payment_amount) <= 0) return setError('请输入每期租金')
    }
    if (step === 2) {
      if (!formData.discount_rate || Number(formData.discount_rate) < 0) return setError('请输入折现率')
    }
    return true
  }

  const handleNext = () => {
    if (validateStep() !== true) return
    if (step < STEPS.length - 1) setStep(step + 1)
  }

  const handlePrev = () => {
    if (step > 0) setStep(step - 1)
  }

  const handleSubmit = async () => {
    setSubmitting(true)
    setError(null)
    try {
      const data = {
        ...formData,
        lease_term_months: Number(formData.lease_term_months),
        payment_amount: Number(formData.payment_amount),
        discount_rate: Number(formData.discount_rate),
        tax_rate: Number(formData.tax_rate),
        initial_direct_costs: Number(formData.initial_direct_costs),
        lease_incentives: Number(formData.lease_incentives),
        residual_value_guarantee: Number(formData.residual_value_guarantee),
        purchase_option_price: formData.purchase_option && formData.purchase_option_price
          ? Number(formData.purchase_option_price)
          : null,
      }
      const leaseInput = await createLeaseInput(data)
      setCurrentLeaseInput(leaseInput)
      navigate(`/results/${leaseInput.id}`)
    } catch (err: any) {
      setError(err.message || '提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">手动填写租赁信息</h1>

      {/* Step indicator */}
      <div className="flex items-center mb-8">
        {STEPS.map((label, idx) => (
          <div key={label} className="flex items-center flex-1">
            <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium ${
              idx <= step ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-500'
            }`}>
              {idx < step ? <Check className="w-4 h-4" /> : idx + 1}
            </div>
            <span className={`ml-2 text-sm ${idx <= step ? 'text-gray-900 font-medium' : 'text-gray-400'}`}>
              {label}
            </span>
            {idx < STEPS.length - 1 && (
              <div className={`flex-1 h-0.5 mx-4 ${idx < step ? 'bg-primary-600' : 'bg-gray-200'}`} />
            )}
          </div>
        ))}
      </div>

      <div className="card">
        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">{error}</div>
        )}

        {step === 0 && (
          <div className="space-y-4">
            <div>
              <label className="label">租赁名称 *</label>
              <input
                className="input-field"
                value={formData.lease_name}
                onChange={(e) => updateField('lease_name', e.target.value)}
                placeholder="如：办公楼租赁合同"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">租赁开始日 *</label>
                <input
                  type="date"
                  className="input-field"
                  value={formData.lease_commencement_date}
                  onChange={(e) => updateField('lease_commencement_date', e.target.value)}
                />
              </div>
              <div>
                <label className="label">租赁期限（月）*</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.lease_term_months}
                  onChange={(e) => updateField('lease_term_months', e.target.value)}
                  min={1}
                />
              </div>
            </div>
            <div>
              <label className="label">适用准则</label>
              <select
                className="input-field"
                value={formData.standard}
                onChange={(e) => updateField('standard', e.target.value)}
              >
                <option value="IFRS16">IFRS 16</option>
                <option value="ASC842">ASC 842</option>
              </select>
            </div>
          </div>
        )}

        {step === 1 && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">付款周期 *</label>
                <select
                  className="input-field"
                  value={formData.payment_frequency}
                  onChange={(e) => updateField('payment_frequency', e.target.value)}
                >
                  <option value="monthly">月付</option>
                  <option value="quarterly">季付</option>
                  <option value="annual">年付</option>
                </select>
              </div>
              <div>
                <label className="label">付款时点</label>
                <select
                  className="input-field"
                  value={formData.payment_timing}
                  onChange={(e) => updateField('payment_timing', e.target.value)}
                >
                  <option value="end">期末付款</option>
                  <option value="beginning">期初付款</option>
                </select>
              </div>
            </div>
            <div>
              <label className="label">每期租金（不含税）*</label>
              <input
                type="number"
                className="input-field"
                value={formData.payment_amount}
                onChange={(e) => updateField('payment_amount', e.target.value)}
                placeholder="0.00"
                min={0}
                step={0.01}
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">折现率（年利率）*</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.discount_rate}
                  onChange={(e) => updateField('discount_rate', e.target.value)}
                  placeholder="0.05"
                  min={0}
                  max={1}
                  step={0.0001}
                />
                <p className="text-xs text-gray-400 mt-1">如 5% 请输入 0.05</p>
              </div>
              <div>
                <label className="label">税率</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.tax_rate}
                  onChange={(e) => updateField('tax_rate', e.target.value)}
                  placeholder="0"
                  min={0}
                  max={1}
                  step={0.0001}
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">初始直接费用</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.initial_direct_costs}
                  onChange={(e) => updateField('initial_direct_costs', e.target.value)}
                  placeholder="0"
                  min={0}
                  step={0.01}
                />
              </div>
              <div>
                <label className="label">租赁激励</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.lease_incentives}
                  onChange={(e) => updateField('lease_incentives', e.target.value)}
                  placeholder="0"
                  min={0}
                  step={0.01}
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">复原成本/担保余值</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.residual_value_guarantee}
                  onChange={(e) => updateField('residual_value_guarantee', e.target.value)}
                  placeholder="0"
                  min={0}
                  step={0.01}
                />
              </div>
              <div>
                <label className="label">购买选择权价格</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.purchase_option_price}
                  onChange={(e) => updateField('purchase_option_price', e.target.value)}
                  placeholder="0"
                  min={0}
                  step={0.01}
                />
              </div>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">请确认以下信息</h3>
            <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
              <div className="flex justify-between"><span className="text-gray-500">租赁名称</span><span>{formData.lease_name}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">开始日</span><span>{formData.lease_commencement_date}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">期限</span><span>{formData.lease_term_months} 个月</span></div>
              <div className="flex justify-between"><span className="text-gray-500">每期租金</span><span>{formData.payment_amount}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">折现率</span><span>{(Number(formData.discount_rate) * 100).toFixed(4)}%</span></div>
              <div className="flex justify-between"><span className="text-gray-500">准则</span><span>{formData.standard}</span></div>
            </div>
          </div>
        )}

        <div className="flex justify-between mt-6">
          <button
            onClick={handlePrev}
            disabled={step === 0}
            className="btn-secondary flex items-center disabled:opacity-50"
          >
            <ChevronLeft className="w-4 h-4 mr-1" />
            上一步
          </button>
          {step < STEPS.length - 1 ? (
            <button onClick={handleNext} className="btn-primary flex items-center">
              下一步
              <ChevronRight className="w-4 h-4 ml-1" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="btn-primary flex items-center disabled:opacity-50"
            >
              {submitting ? '提交中...' : '确认并计算'}
              <Check className="w-4 h-4 ml-1" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
