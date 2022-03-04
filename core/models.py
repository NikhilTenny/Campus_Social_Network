
from django.db import models
from django.urls import reverse
from users.models import CustomeUsers
from django.utils.text import slugify

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

    def __str__(self):
        return self.Title
