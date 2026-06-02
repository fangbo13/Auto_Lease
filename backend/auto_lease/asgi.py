"""
ASGI config for auto_lease project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_lease.settings')

application = get_asgi_application()
