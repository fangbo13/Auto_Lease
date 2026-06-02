from django.db import models
from core.models import AbstractTimestampModel


class CalculationResult(AbstractTimestampModel):
    lease_input = models.OneToOneField(
        'lease_input.LeaseInput',
        on_delete=models.CASCADE,
        related_name='calculation_result',
        verbose_name='关联租赁输入'
    )
    right_of_use_asset = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='使用权资产'
    )
    lease_liability = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='租赁负债'
    )
    total_payments = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='总付款额'
    )
    total_interest = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='总利息费用'
    )
    total_depreciation = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='总折旧费用'
    )
    first_month_interest = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='首月利息'
    )
    first_month_depreciation = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='首月折旧'
    )
    effective_monthly_rate = models.DecimalField(
        max_digits=10, decimal_places=8, verbose_name='实际月利率'
    )
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name='计算时间')

    class Meta:
        db_table = 'calculation_results'
        verbose_name = '计算结果'
        verbose_name_plural = '计算结果'

    def __str__(self):
        return f"{self.lease_input.lease_name} 计算结果"


class AmortizationSchedule(AbstractTimestampModel):
    calculation_result = models.ForeignKey(
        CalculationResult,
        on_delete=models.CASCADE,
        related_name='schedule',
        verbose_name='关联计算结果'
    )
    period_number = models.PositiveIntegerField(verbose_name='期次')
    period_start_date = models.DateField(verbose_name='期初日期')
    period_end_date = models.DateField(verbose_name='期末日期')
    opening_liability = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='期初负债'
    )
    payment_amount = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='付款额'
    )
    interest_expense = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='利息费用'
    )
    principal_reduction = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='本金偿还'
    )
    closing_liability = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='期末负债'
    )
    rou_asset_opening = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='期初使用权资产'
    )
    depreciation_expense = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='折旧费用'
    )
    rou_asset_closing = models.DecimalField(
        max_digits=20, decimal_places=4, verbose_name='期末使用权资产'
    )

    class Meta:
        db_table = 'amortization_schedules'
        verbose_name = '摊销明细'
        verbose_name_plural = '摊销明细'
        ordering = ['calculation_result', 'period_number']
        unique_together = ['calculation_result', 'period_number']

    def __str__(self):
        return f"第{self.period_number}期"
