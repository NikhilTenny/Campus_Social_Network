from django.urls import re_path
from chat import consumers


websocket_urlpatterns = [
            re_path(r'ws/home/chats/(?P<username>\w+)/$', consumers.PersonalChatCon.as_asgi()),
        ]