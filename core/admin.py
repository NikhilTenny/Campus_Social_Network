from django.contrib import admin
from .models import Posts, FriendRequest, Friends
# Register your models here

admin.site.register(Posts)
admin.site.register(FriendRequest)
admin.site.register(Friends)


