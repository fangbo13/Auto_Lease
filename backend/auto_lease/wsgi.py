"""
WSGI config for auto_lease project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_lease.settings')

application = get_wsgi_application()
