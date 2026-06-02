from django.test import TestCase
from audit_trail.models import AuditTrail


class AuditTrailTests(TestCase):
    def test_create_audit_trail(self):
        trail = AuditTrail.objects.create(
            action='upload',
            entity_type='Contract',
            entity_id='123e4567-e89b-12d3-a456-426614174000',
            details={'file_name': 'test.pdf'},
        )
        self.assertEqual(trail.action, 'upload')
        self.assertEqual(str(trail), '上传 Contract 123e4567-e89b-12d3-a456-426614174000')
