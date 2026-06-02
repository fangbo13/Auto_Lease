import { apiClient } from './client'
import { Contract } from '../types'

export const uploadContract = async (file: File, parser?: string): Promise<Contract> => {
  const formData = new FormData()
  formData.append('original_file', file)
  if (parser) {
    formData.append('parser', parser)
  }
  const response = await apiClient.post('/contracts/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const parseContract = async (contractId: string, parser?: string) => {
  const response = await apiClient.post(`/contracts/${contractId}/parse/`, { parser })
  return response.data
}

export const getContracts = async (): Promise<Contract[]> => {
  const response = await apiClient.get('/contracts/')
  return response.data.results || response.data
}
