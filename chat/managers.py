from django.db import models
from django.db.models import Count

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


    