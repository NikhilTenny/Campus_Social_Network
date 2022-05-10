from django.urls import path
from . import views as chat_view
urlpatterns = [
    path('home/chats/', chat_view.PersonalChatsView.as_view(), name='chatlist'),    # List all the personal chats
    path('home/chats/<str:username>/', chat_view.ChattingView, name='chat'),        # A personal chat
    path('home/chats/<str:username>/clearchat', chat_view.ClearChatView, name='clearchat'), # Clear chat
    path('home/discussion_rooms/',                      # List all room
          chat_view.Dis_roomsView.as_view(), 
          name='dis_rooms'
    ),     
    path('home/discussion_rooms/create',                # Create a room 
         chat_view.Dis_roomCreateView, 
         name="create_dis_room"
    ), 
    path(                                                           
        'home/discussion_rooms/<int:id>/<username>/',   # Discussion room
        chat_view.Dis_roomView, 
        name='dis_room'
    ),
    path(
        'home/discussion_rooms/<int:id>/details',              # Discussion room details
        chat_view.Dis_room_detailsView,
        name='room_details'
    ) ,
    path('home/discussion_rooms/edit/<int:id>/',        # Edit room            
        chat_view.dis_room_editView, 
        name='room_edit_dis' 
    ),
    path('home/discussion_rooms/<int:id>/remove/<str:username>/',   #Remove a member from room
        chat_view.dis_room_remView,
        name='remove_member'
    ),
    path('home/discussion_rooms/<int:id>/add/<str:username>/',      #Add a member to room
        chat_view.dis_room_addView,
        name='add_room_member'
    )
]