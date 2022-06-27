"""
WSGI config for shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
# 生产环境的实现在这
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings.productsetting')
application = get_wsgi_application()
