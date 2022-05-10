from django.db import models
from django.db.models import Count

from users.models import CustomeUsers
from django.db.models import Q

class ChatSpaceManager(models.Manager):
    # Return all the personal chats of a user
    def get_userchat(self, user):
        chats = self.get_queryset().filter(type='personal')
        chats = chats.filter(users__in=[user])
        # chats = chats.annotate(u_count=Count('users')).filter(u_count=2) 
        return chats

    def get_or_create_chat(self, user, other_user):
        # Search for a personal chatspace with given users 
        chat = self.get_queryset().filter(type='personal') 
        chat = chat.filter(users__in=[user, other_user]).distinct()
        chat = chat.annotate(u_count=Count('users')).filter(u_count=2)
        # If is doesn't exist new chatspace is created 
        if chat.exists():
            return chat.first()
        else:
            chat = self.create(type='personal')
            chat.users.add(user)
            chat.users.add(other_user)
            return chat
    # Get the list of users not in the discussion room
    def get_members_not_in_room(self,id):
        room = self.get(id=id)
        users = CustomeUsers.objects.filter(~Q(is_superuser=True))
        u=[]
        in_room = room.users.all()
        for user in users:
            if user in in_room:
                continue
            u.append(user)
        return u  

    # Find the list of rooms that the user is in 
    def users_rooms(self,user):
        rooms = self.get_queryset().filter(type='chatroom') 
        user_in_rooms = []
        for room in rooms:
            users = room.users.all()
            if user in users:
                user_in_rooms.append(room)
        return user_in_rooms     





        


    