from django.test import TestCase
from decimal import Decimal
from lease_input.models import LeaseInput
from calculations.services.ifrs16_engine import IFRS16Engine


class IFRS16EngineTests(TestCase):
    def test_calculate_lease_liability(self):
        """测试已知案例：年付款 10 万，5 年期，5% 折现率，期末付款。"""
        li = LeaseInput.objects.create(
            lease_name='测试',
            lease_commencement_date='2024-01-01',
            lease_term_months=60,
            payment_frequency='monthly',
            payment_amount=Decimal('8333.3333'),  # 10万/年 ≈ 8333.33/月
            discount_rate=Decimal('0.05'),
            payment_timing='end',
        )
        engine = IFRS16Engine(li)
        result = engine.calculate()

        self.assertIn('lease_liability', result)
        self.assertIn('right_of_use_asset', result)
        self.assertIn('schedule', result)
        self.assertEqual(len(result['schedule']), 60)

        # 验证摊销表最后一期负债为 0
        last_period = result['schedule'][-1]
        self.assertEqual(last_period['closing_liability'], Decimal('0'))

    def test_beginning_of_period_payment(self):
        li = LeaseInput.objects.create(
            lease_name='期初付款测试',
            lease_commencement_date='2024-01-01',
            lease_term_months=12,
            payment_frequency='monthly',
            payment_amount=Decimal('10000'),
            discount_rate=Decimal('0.06'),
            payment_timing='beginning',
        )
        engine = IFRS16Engine(li)
        result = engine.calculate()
        self.assertEqual(len(result['schedule']), 12)
