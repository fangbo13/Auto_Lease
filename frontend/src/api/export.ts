import { apiClient } from './client'

export const exportWorkingPaper = async (leaseInputId: string): Promise<Blob> => {
  const response = await apiClient.get(`/export/working-paper/?lease_input_id=${leaseInputId}`, {
    responseType: 'blob',
  })
  return response.data
}
