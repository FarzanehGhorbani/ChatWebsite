from django.urls import re_path
from .consumers import ChatConsumer,ConnectConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$',ConnectConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$',ChatConsumer.as_asgi()),
    # as_asgi() : for each user create uniqe ChatConsumer
]