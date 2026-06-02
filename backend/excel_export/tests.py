from django.test import TestCase
from decimal import Decimal
from lease_input.models import LeaseInput
from calculations.models import CalculationResult
from excel_export.services.chinese_audit_wp import ChineseAuditWorkingPaperGenerator


class ExcelExportTests(TestCase):
    def test_generate_excel(self):
        li = LeaseInput.objects.create(
            lease_name='Excel测试',
            lease_commencement_date='2024-01-01',
            lease_term_months=12,
            payment_frequency='monthly',
            payment_amount=Decimal('10000'),
            discount_rate=Decimal('0.05'),
        )
        calc = CalculationResult.objects.create(
            lease_input=li,
            right_of_use_asset=Decimal('100000'),
            lease_liability=Decimal('100000'),
            total_payments=Decimal('120000'),
            total_interest=Decimal('20000'),
            total_depreciation=Decimal('100000'),
            first_month_interest=Decimal('400'),
            first_month_depreciation=Decimal('8333.33'),
            effective_monthly_rate=Decimal('0.004074'),
        )

        generator = ChineseAuditWorkingPaperGenerator()
        excel_bytes = generator.generate(li, calc)

        self.assertIsInstance(excel_bytes, bytes)
        self.assertTrue(len(excel_bytes) > 0)
