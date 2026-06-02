import { create } from 'zustand'
import { LeaseInput, CalculationResult, Contract } from '../types'

interface AppState {
  contracts: Contract[]
  currentLeaseInput: LeaseInput | null
  calculationResult: CalculationResult | null
  isLoading: boolean
  error: string | null
  setContracts: (contracts: Contract[]) => void
  setCurrentLeaseInput: (input: LeaseInput | null) => void
  setCalculationResult: (result: CalculationResult | null) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useAppStore = create<AppState>((set) => ({
  contracts: [],
  currentLeaseInput: null,
  calculationResult: null,
  isLoading: false,
  error: null,
  setContracts: (contracts) => set({ contracts }),
  setCurrentLeaseInput: (currentLeaseInput) => set({ currentLeaseInput }),
  setCalculationResult: (calculationResult) => set({ calculationResult }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}))
