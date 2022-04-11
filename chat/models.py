from django.db import models
from users.models import CustomeUsers
from .managers import ChatSpaceManager


# Store the type of chat and the users in it
class ChatSpace(models.Model):
    chat_type = (('personal','Personal'),
                  ('chatroom','Chat Room'))
    name = models.CharField(max_length=50, null=True, blank=True) 
    description = models.CharField(max_length=200, null=True, blank=True)                 
    type = models.CharField(max_length=20, choices=chat_type, default='chatroom')                  
    users = models.ManyToManyField(CustomeUsers)
    created = models.DateTimeField(auto_now_add=True)
 
    objects = ChatSpaceManager()

    def __str__(self):
        if self.type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'


# Store all the messages send in both personal and group chat
class Message(models.Model):
    chat = models.ForeignKey(ChatSpace, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomeUsers, on_delete=models.CASCADE)
    body = models.CharField(max_length=600)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username 

    class Meta:
        ordering = ['created']    




