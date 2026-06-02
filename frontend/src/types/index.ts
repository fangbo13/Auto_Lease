export interface Contract {
  id: string
  original_file: string
  file_name: string
  file_size: number
  mime_type: string
  parsed_status: 'uploaded' | 'parsing' | 'success' | 'failed'
  parser_used: string
  parsed_data: Record<string, unknown>
  created_at: string
}

export interface LeaseInput {
  id: string
  contract: string | null
  lease_name: string
  lease_commencement_date: string
  lease_term_months: number
  payment_frequency: 'monthly' | 'quarterly' | 'annual'
  payment_amount: number
  payment_timing: 'beginning' | 'end'
  discount_rate: number
  discount_rate_type: 'incremental_borrowing' | 'implicit_rate'
  tax_rate: number
  initial_direct_costs: number
  lease_incentives: number
  residual_value_guarantee: number
  purchase_option: boolean
  purchase_option_price: number | null
  standard: 'IFRS16' | 'ASC842'
  notes: string
  created_at: string
  updated_at: string
}

export interface CalculationResult {
  id: string
  lease_input: string
  right_of_use_asset: number
  lease_liability: number
  total_payments: number
  total_interest: number
  total_depreciation: number
  first_month_interest: number
  first_month_depreciation: number
  effective_monthly_rate: number
  calculated_at: string
}

export interface AmortizationScheduleItem {
  id: string
  period_number: number
  period_start_date: string
  period_end_date: string
  opening_liability: number
  payment_amount: number
  interest_expense: number
  principal_reduction: number
  closing_liability: number
  rou_asset_opening: number
  depreciation_expense: number
  rou_asset_closing: number
}
