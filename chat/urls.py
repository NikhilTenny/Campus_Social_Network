from django.urls import path
from . import views as chat_view
urlpatterns = [
    path('home/chats/', chat_view.PersonalChatsView.as_view(), name='chatlist'),    # List all the personal chats
    path('home/chats/<str:username>/', chat_view.ChattingView, name='chat'),        # A personal chat
    path('home/chats/<str:username>/clearchat', chat_view.ClearChatView, name='clearchat'), # Clear chat
    path('home/discussion_rooms/',              # List all room
          chat_view.Dis_roomsView.as_view(), 
          name='dis_rooms'
    ),     
    path('home/discussion_rooms/create',        # Create a room 
         chat_view.Dis_roomCreateView, 
         name="create_dis_room"
    ), 
    path(                                                           
        'home/discussion_rooms/<int:id>/<username>/',      # Discussion room
        chat_view.Dis_roomView, 
        name='dis_room'
    )
]