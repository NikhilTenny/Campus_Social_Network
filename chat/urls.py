from django.urls import path
from . import views as chat_view
urlpatterns = [
    path('home/chats/',chat_view.PersonalChatsView.as_view(), name='chatlist'),
    path('home/chats/<str:username>/', chat_view.ChattingView, name='chat'),
    path('home/chats/<str:username>/clearchat',chat_view.ClearChatView, name='clearchat'),
]