import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileCheck, AlertTriangle, Loader2 } from 'lucide-react'
import { uploadContract, parseContract } from '../api/contracts'
import { createLeaseInput } from '../api/leaseInputs'
import { useAppStore } from '../store/appStore'

const PARSERS = [
  { value: '', label: '默认解析器' },
  { value: 'gpt4vision', label: 'GPT-4 Vision' },
  { value: 'qwen', label: 'Qwen-VL' },
  { value: 'tesseract', label: 'Tesseract OCR' },
]

export default function ContractUpload() {
  const navigate = useNavigate()
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [parsing, setParsing] = useState(false)
  const [selectedParser, setSelectedParser] = useState('')
  const [parseResult, setParseResult] = useState<Record<string, unknown> | null>(null)
  const [contractId, setContractId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const setCurrentLeaseInput = useAppStore((s) => s.setCurrentLeaseInput)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file: File) => {
    setError(null)
    setParseResult(null)
    setUploading(true)
    try {
      const contract = await uploadContract(file, selectedParser)
      setContractId(contract.id)
      setUploading(false)
      setParsing(true)
      const result = await parseContract(contract.id, selectedParser)
      setParseResult(result.data)
    } catch (err: any) {
      setError(err.message || '上传或解析失败')
    } finally {
      setUploading(false)
      setParsing(false)
    }
  }

  const handleCreateFromParse = async () => {
    if (!parseResult) return
    try {
      const data = {
        lease_name: (parseResult.lease_name as string) || '未命名租赁',
        lease_commencement_date: parseResult.lease_commencement_date || new Date().toISOString().split('T')[0],
        lease_term_months: Number(parseResult.lease_term_months) || 12,
        payment_frequency: (parseResult.payment_frequency as string) || 'monthly',
        payment_amount: Number(parseResult.payment_amount) || 0,
        payment_timing: (parseResult.payment_timing as string) || 'end',
        discount_rate: Number(parseResult.discount_rate) || 0.05,
        discount_rate_type: 'incremental_borrowing',
        tax_rate: Number(parseResult.tax_rate) || 0,
        initial_direct_costs: Number(parseResult.initial_direct_costs) || 0,
        lease_incentives: Number(parseResult.lease_incentives) || 0,
        residual_value_guarantee: Number(parseResult.residual_value_guarantee) || 0,
        purchase_option: Boolean(parseResult.purchase_option),
        purchase_option_price: parseResult.purchase_option_price ? Number(parseResult.purchase_option_price) : null,
        standard: (parseResult.standard as string) || 'IFRS16',
      }
      const leaseInput = await createLeaseInput(data)
      setCurrentLeaseInput(leaseInput)
      navigate(`/results/${leaseInput.id}`)
    } catch (err: any) {
      setError(err.message || '创建失败')
    }
  }

  const getConfidenceColor = (score?: number) => {
    if (!score) return 'text-gray-400'
    if (score >= 0.8) return 'text-green-600'
    if (score >= 0.5) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">上传租赁合同</h1>

      <div className="card space-y-4">
        <div>
          <label className="label">选择解析器</label>
          <select
            className="input-field max-w-xs"
            value={selectedParser}
            onChange={(e) => setSelectedParser(e.target.value)}
          >
            {PARSERS.map((p) => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>
        </div>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-2">
            拖拽文件到此处，或 <span className="text-primary-600 font-medium">点击上传</span>
          </p>
          <p className="text-xs text-gray-400">支持 PDF、PNG、JPG 格式，最大 20MB</p>
          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileInput}
            className="hidden"
            id="file-input"
          />
          <label htmlFor="file-input" className="absolute inset-0 cursor-pointer" />
        </div>

        {(uploading || parsing) && (
          <div className="flex items-center justify-center space-x-2 text-primary-600">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>{uploading ? '上传中...' : 'AI 解析中...'}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-md">
            <AlertTriangle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {parseResult && (
        <div className="card space-y-4">
          <div className="flex items-center space-x-2">
            <FileCheck className="w-5 h-5 text-green-600" />
            <h2 className="text-lg font-semibold">解析结果</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(parseResult)
              .filter(([key]) => !['confidence_score', 'field_confidence', 'parsed_text'].includes(key))
              .map(([key, value]) => {
                const confidence = (parseResult.field_confidence as Record<string, number>)?.[key]
                return (
                  <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <span className="text-sm text-gray-600">{key}</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-900">
                        {value === null || value === undefined ? '-' : String(value)}
                      </span>
                      {confidence !== undefined && (
                        <span className={`text-xs ${getConfidenceColor(confidence)}`}>
                          {Math.round(confidence * 100)}%
                        </span>
                      )}
                    </div>
                  </div>
                )
              })}
          </div>

          <div className="flex space-x-3">
            <button onClick={handleCreateFromParse} className="btn-primary flex-1">
              确认并计算
            </button>
            <button onClick={() => navigate('/manual')} className="btn-secondary flex-1">
              手动修改
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
