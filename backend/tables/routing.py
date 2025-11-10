from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/tables/$', consumers.tableStatusConsumer.as_asgi()),
    re_path(r'^ws/orders/$', consumers.ordersConsumer.as_asgi()),
]