from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
from typing import List, Dict, Any


class IFRS16Engine:
    """IFRS 16 租赁计算引擎。"""

    def __init__(self, lease_input):
        self.lease_input = lease_input

    def calculate(self) -> Dict[str, Any]:
        li = self.lease_input
        annual_rate = Decimal(str(li.discount_rate))
        monthly_rate = self._annual_to_monthly_rate(annual_rate)
        term = int(li.lease_term_months)
        payment = Decimal(str(li.payment_amount))
        frequency = li.payment_frequency
        timing = li.payment_timing

        # 根据付款频率计算每期付款额和实际期数
        periods, periodic_payment = self._normalize_payment_terms(term, payment, frequency)
        periodic_rate = self._normalize_rate(monthly_rate, frequency)

        # 计算租赁负债（现值）
        lease_liability = self._calculate_lease_liability(
            periodic_payment, periodic_rate, periods, timing
        )

        # 计算使用权资产
        initial_costs = Decimal(str(li.initial_direct_costs))
        incentives = Decimal(str(li.lease_incentives))
        residual = Decimal(str(li.residual_value_guarantee))
        purchase_price = Decimal(str(li.purchase_option_price)) if li.purchase_option and li.purchase_option_price else Decimal('0')

        rou_asset = lease_liability + initial_costs - incentives + residual + purchase_price

        # 生成摊销表
        schedule = self._generate_schedule(
            lease_liability, rou_asset, periodic_payment,
            periodic_rate, periods, timing, li.lease_commencement_date, frequency
        )

        total_payments = periodic_payment * periods
        total_interest = sum(row['interest_expense'] for row in schedule)
        total_depreciation = sum(row['depreciation_expense'] for row in schedule)

        return {
            'right_of_use_asset': rou_asset.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            'lease_liability': lease_liability.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            'total_payments': total_payments.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            'total_interest': total_interest.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            'total_depreciation': total_depreciation.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            'first_month_interest': schedule[0]['interest_expense'].quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP) if schedule else Decimal('0'),
            'first_month_depreciation': schedule[0]['depreciation_expense'].quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP) if schedule else Decimal('0'),
            'effective_monthly_rate': monthly_rate.quantize(Decimal('0.00000001'), rounding=ROUND_HALF_UP),
            'schedule': schedule,
        }

    def _annual_to_monthly_rate(self, annual_rate: Decimal) -> Decimal:
        """将年利率转为月利率。"""
        return (Decimal('1') + annual_rate) ** (Decimal('1') / Decimal('12')) - Decimal('1')

    def _normalize_payment_terms(self, term_months: int, monthly_payment: Decimal, frequency: str):
        """根据付款频率标准化付款条件。"""
        if frequency == 'monthly':
            return term_months, monthly_payment
        elif frequency == 'quarterly':
            periods = term_months // 3
            return periods, monthly_payment * Decimal('3')
        elif frequency == 'annual':
            periods = term_months // 12
            return periods, monthly_payment * Decimal('12')
        return term_months, monthly_payment

    def _normalize_rate(self, monthly_rate: Decimal, frequency: str) -> Decimal:
        """根据付款频率计算期间利率。"""
        if frequency == 'monthly':
            return monthly_rate
        elif frequency == 'quarterly':
            return (Decimal('1') + monthly_rate) ** Decimal('3') - Decimal('1')
        elif frequency == 'annual':
            return (Decimal('1') + monthly_rate) ** Decimal('12') - Decimal('1')
        return monthly_rate

    def _calculate_lease_liability(self, payment: Decimal, rate: Decimal, periods: int, timing: str) -> Decimal:
        """计算租赁负债现值。"""
        if rate == 0:
            return payment * periods

        if timing == 'beginning':
            # 期初付款：第一期立即支付，剩余 n-1 期按普通年金折现
            if periods == 0:
                return Decimal('0')
            pv = payment
            if periods > 1:
                pv += payment * ((Decimal('1') - (Decimal('1') + rate) ** (-(periods - 1))) / rate)
            return pv
        else:
            # 期末付款：普通年金
            return payment * ((Decimal('1') - (Decimal('1') + rate) ** (-periods)) / rate)

    def _generate_schedule(self, lease_liability: Decimal, rou_asset: Decimal,
                           payment: Decimal, rate: Decimal, periods: int,
                           timing: str, start_date, frequency: str) -> List[Dict[str, Any]]:
        """生成摊销明细表。"""
        schedule = []
        opening_liability = lease_liability
        rou_balance = rou_asset
        depreciation_per_period = (rou_asset / periods).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

        # 计算每期月份跨度
        if frequency == 'monthly':
            months_delta = 1
        elif frequency == 'quarterly':
            months_delta = 3
        else:
            months_delta = 12

        for i in range(1, periods + 1):
            if timing == 'beginning':
                # 期初付款：付款在期初，利息基于付款后的余额
                if i == 1:
                    interest = (opening_liability - payment) * rate
                else:
                    interest = opening_liability * rate
                principal = payment - interest
            else:
                # 期末付款
                interest = opening_liability * rate
                principal = payment - interest

            interest = interest.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            principal = principal.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            closing_liability = (opening_liability - principal).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

            # 处理最后一期的尾差
            if i == periods:
                principal = opening_liability
                closing_liability = Decimal('0')

            period_start = self._add_months(start_date, (i - 1) * months_delta)
            period_end = self._add_months(start_date, i * months_delta) - timedelta(days=1)

            schedule.append({
                'period_number': i,
                'period_start_date': period_start,
                'period_end_date': period_end,
                'opening_liability': opening_liability.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
                'payment_amount': payment.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
                'interest_expense': interest,
                'principal_reduction': principal,
                'closing_liability': closing_liability,
                'rou_asset_opening': rou_balance.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
                'depreciation_expense': depreciation_per_period,
                'rou_asset_closing': (rou_balance - depreciation_per_period).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            })

            opening_liability = closing_liability
            rou_balance -= depreciation_per_period

        return schedule

    @staticmethod
    def _add_months(source_date, months):
        from datetime import date
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, [31, 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28,
                                     31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return date(year, month, day)
