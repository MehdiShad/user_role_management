"""
ASGI config for ExhibitionProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from django.urls import path

from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.base')

application = get_asgi_application()

