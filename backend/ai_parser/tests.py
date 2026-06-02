from django.test import TestCase
from .base import AbstractAIParser
from .registry import ParserRegistry, get_active_parser


class MockParser(AbstractAIParser):
    def parse(self, file_path, mime_type):
        return {'lease_commencement_date': '2024-01-01', 'lease_term_months': 12}

    def get_name(self):
        return 'mock'

    def supports(self, mime_type):
        return True


class AIParserTests(TestCase):
    def test_registry(self):
        ParserRegistry.register('mock', MockParser)
        parser = ParserRegistry.get_parser('mock')
        self.assertIsInstance(parser, MockParser)
        self.assertIn('mock', ParserRegistry.list_parsers())

    def test_validate_output(self):
        parser = MockParser()
        valid = {'lease_commencement_date': '2024-01-01', 'lease_term_months': 12, 'payment_amount': 1000}
        self.assertTrue(parser.validate_output(valid))

        invalid = {'lease_name': 'test'}
        self.assertFalse(parser.validate_output(invalid))
