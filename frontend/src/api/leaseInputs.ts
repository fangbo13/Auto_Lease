import { apiClient } from './client'
import { LeaseInput } from '../types'

export const createLeaseInput = async (data: Partial<LeaseInput>): Promise<LeaseInput> => {
  const response = await apiClient.post('/lease-inputs/', data)
  return response.data
}

export const updateLeaseInput = async (id: string, data: Partial<LeaseInput>): Promise<LeaseInput> => {
  const response = await apiClient.put(`/lease-inputs/${id}/`, data)
  return response.data
}

export const getLeaseInput = async (id: string): Promise<LeaseInput> => {
  const response = await apiClient.get(`/lease-inputs/${id}/`)
  return response.data
}

export const triggerCalculation = async (id: string) => {
  const response = await apiClient.post(`/lease-inputs/${id}/calculate/`)
  return response.data
}
