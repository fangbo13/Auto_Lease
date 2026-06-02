from django.test import TestCase
from .models import LeaseInput


class LeaseInputModelTests(TestCase):
    def test_create_lease_input(self):
        li = LeaseInput.objects.create(
            lease_name='测试租赁',
            lease_commencement_date='2024-01-01',
            lease_term_months=36,
            payment_frequency='monthly',
            payment_amount=50000,
            discount_rate=0.05,
        )
        self.assertEqual(str(li), '测试租赁')
        self.assertEqual(li.standard, 'IFRS16')
