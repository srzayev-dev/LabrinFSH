from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path
from core.consumers import ChatConsumer


application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('detail/<int:file_id>', ChatConsumer.as_asgi())
                ]
            )
        )
    )
})