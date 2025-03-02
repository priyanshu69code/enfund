from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'wss/chat/(?P<group_name>\w+)/$', ChatConsumer.as_asgi()),
]
