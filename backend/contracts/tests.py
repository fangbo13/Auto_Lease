from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Contract


class ContractModelTests(TestCase):
    def test_create_contract(self):
        file = SimpleUploadedFile('test.pdf', b'PDF content', content_type='application/pdf')
        contract = Contract.objects.create(
            original_file=file,
            file_name='test.pdf',
            file_size=12,
            mime_type='application/pdf',
        )
        self.assertEqual(contract.file_name, 'test.pdf')
        self.assertEqual(contract.parsed_status, 'uploaded')
