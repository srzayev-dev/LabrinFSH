from django.urls import url
from django.conf.urls import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from core.consumers import ChatConsumer


application = ProtocolTypeRouter({
    'websocket' : AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            [
                url(r"^(?P<username>[\w.@+-]+)", ChatConsumer),
            ]
        )
    )
})