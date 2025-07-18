"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# config/wsgi.py ni tekshiring va yangilang

import os
from django.core.wsgi import get_wsgi_application
# Production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()

# Vercel uchun
app = application