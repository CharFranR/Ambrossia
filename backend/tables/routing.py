from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # Acepta con y sin barra final y ancla el patrón al inicio/fin
    re_path(r'^ws/socket-server/?$', consumers.tableStatusConsumer.as_asgi()),
]