from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AbstractTimestampModel


class LeaseInput(AbstractTimestampModel):
    STANDARD_CHOICES = [
        ('IFRS16', 'IFRS 16'),
        ('ASC842', 'ASC 842'),
    ]

    FREQUENCY_CHOICES = [
        ('monthly', '月付'),
        ('quarterly', '季付'),
        ('annual', '年付'),
    ]

    PAYMENT_TIMING_CHOICES = [
        ('beginning', '期初付款'),
        ('end', '期末付款'),
    ]

    RATE_TYPE_CHOICES = [
        ('incremental_borrowing', '增量借款利率'),
        ('implicit_rate', '租赁内含利率'),
    ]

    contract = models.OneToOneField(
        'contracts.Contract',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='关联合同'
    )
    lease_name = models.CharField(max_length=255, verbose_name='租赁名称')
    lease_commencement_date = models.DateField(verbose_name='租赁开始日')
    lease_term_months = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)],
        verbose_name='租赁期限(月)'
    )
    payment_frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='monthly',
        verbose_name='付款周期'
    )
    payment_amount = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        validators=[MinValueValidator(0)],
        verbose_name='每期租金(不含税)'
    )
    payment_timing = models.CharField(
        max_length=20,
        choices=PAYMENT_TIMING_CHOICES,
        default='end',
        verbose_name='付款时点'
    )
    discount_rate = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name='折现率(年)'
    )
    discount_rate_type = models.CharField(
        max_length=30,
        choices=RATE_TYPE_CHOICES,
        default='incremental_borrowing',
        verbose_name='折现率类型'
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name='税率'
    )
    initial_direct_costs = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=0,
        verbose_name='初始直接费用'
    )
    lease_incentives = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=0,
        verbose_name='租赁激励'
    )
    residual_value_guarantee = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=0,
        verbose_name='预计复原成本/担保余值'
    )
    purchase_option = models.BooleanField(default=False, verbose_name='购买选择权')
    purchase_option_price = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='购买选择权价格'
    )
    standard = models.CharField(
        max_length=20,
        choices=STANDARD_CHOICES,
        default='IFRS16',
        verbose_name='适用准则'
    )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='创建用户'
    )
    notes = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        db_table = 'lease_inputs'
        verbose_name = '租赁输入'
        verbose_name_plural = '租赁输入'

    def __str__(self):
        return self.lease_name
