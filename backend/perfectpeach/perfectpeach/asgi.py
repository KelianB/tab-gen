"""
ASGI config for perfectpeach project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import converter.urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfectpeach.settings')

# We route HTTP and WS requests differently : HTTP goes to Django, WS goes to Django-Channels.
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
         URLRouter(
              converter.urls.websocket_urlpatterns
         )
    ),
})
