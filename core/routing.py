from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from core.consumers import ChatConsumer


websocket_urlpatterns = ProtocolTypeRouter({
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            [
                path("detail/<int:file_id>", ChatConsumer),
            ]
        )
    )
})