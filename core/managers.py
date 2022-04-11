from django.db import models

class FriendManager(models.Manager):
    def get_friends(self, user):
        friends = self.get_queryset().filter(user1=user) | self.get_queryset().filter(user2=user)
        return friends

    def find_if_friends(self, u1, u2):
        friends = self.get_queryset().filter(user1=u1, user2=u2) |self.get_queryset().filter(user1=u2, user2=u1)    
        return friends