"""
ASGI config for chat project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from core.consumers import ChatConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LabrinFSH.settings')
django.setup()


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r"^(?P<username>[\w.@+-]+)", ChatConsumer),
        ])
    ),
})
