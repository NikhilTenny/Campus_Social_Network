from tkinter.tix import Tree
from django.db import models
from django.urls import reverse
from users.models import CustomeUsers
from django.utils.text import slugify
from .managers import FriendManager

#Store all the timeline,placement and notice board posts
class Posts(models.Model):
    Author = models.ForeignKey(CustomeUsers,on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Content = models.CharField(max_length=1000)
    Picture = models.ImageField(upload_to='posts',blank = True)
    is_timeline = models.BooleanField(default=True)
    is_p_cell = models.BooleanField(default=False)
    is_notice = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True,null=True)

    def get_absolute_url(self):
        return reverse('postdetail',kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Title) 
        super().save(*args, **kwargs)

    # Return all the Notice Board posts    
    @classmethod
    def get_Notice(self):
        posts = self.objects.filter(is_notice = True, is_p_cell = False, is_timeline = False)
        return posts

    # Return all the Timeline posts    
    @classmethod
    def get_Timeline(self):
        posts = self.objects.filter(is_notice = False, is_p_cell = False, is_timeline = True)
        return posts

    # Return all the Placement posts    
    @classmethod
    def get_Placement(self):
        posts = self.objects.filter(is_notice = False, is_p_cell = True, is_timeline = False)
        return posts    


    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-created']    

# Store Friend relationship between users
class Friends(models.Model):
    user1 = models.ForeignKey(CustomeUsers, on_delete=models.CASCADE,related_name='Friend1')
    user2 = models.ForeignKey(CustomeUsers, on_delete=models.CASCADE,related_name='Friend2')
    date = models.DateTimeField(auto_now_add=True)

    objects = FriendManager()

    def __str__(self):
        return f'{self.user1.username} and {self.user2.username}'

# Store the friend requests send from one user to another
class FriendRequest(models.Model):
    reqsender = models.ForeignKey(CustomeUsers, on_delete=models.CASCADE,related_name='senduser')
    reqreceiver = models.ForeignKey(CustomeUsers, on_delete=models.CASCADE,related_name='receiveuser')
    pending = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    senddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reqsender.username} to {self.reqreceiver.username}'

