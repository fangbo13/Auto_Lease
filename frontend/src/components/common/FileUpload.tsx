import { useState, useCallback } from 'react'
import { Upload, X } from 'lucide-react'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  accept?: string
  maxSizeMB?: number
}

export default function FileUpload({ onFileSelect, accept = '.pdf,.png,.jpg,.jpeg', maxSizeMB = 20 }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const validateFile = (file: File): boolean => {
    setError(null)
    if (file.size > maxSizeMB * 1024 * 1024) {
      setError(`文件大小不能超过 ${maxSizeMB}MB`)
      return false
    }
    const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg']
    if (!validTypes.includes(file.type)) {
      setError('仅支持 PDF、PNG、JPG 格式')
      return false
    }
    return true
  }

  const handleFile = (file: File) => {
    if (validateFile(file)) {
      setSelectedFile(file)
      onFileSelect(file)
    }
  }

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
    if (files.length > 0) handleFile(files[0])
  }, [])

  const clearFile = () => {
    setSelectedFile(null)
    setError(null)
  }

  return (
    <div className="w-full">
      {!selectedFile ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            isDragging ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-gray-400'
          }`}
        >
          <Upload className="w-10 h-10 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-600 text-sm">
            拖拽文件到此处，或 <span className="text-primary-600 font-medium">点击上传</span>
          </p>
          <p className="text-xs text-gray-400 mt-1">支持 PDF、PNG、JPG，最大 {maxSizeMB}MB</p>
          <input
            type="file"
            accept={accept}
            onChange={(e) => e.target.files && handleFile(e.target.files[0])}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="absolute inset-0 cursor-pointer" />
        </div>
      ) : (
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
          <div className="flex items-center space-x-3">
            <Upload className="w-5 h-5 text-primary-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
              <p className="text-xs text-gray-500">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
          <button onClick={clearFile} className="p-1 hover:bg-gray-200 rounded">
            <X className="w-4 h-4 text-gray-500" />
          </button>
        </div>
      )}
      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
    </div>
  )
}
