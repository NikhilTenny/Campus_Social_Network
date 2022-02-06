from unicodedata import name
from django.contrib import admin
from django.urls import path
from users import views as U_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',U_views.HomeView,name = 'index'),
    path('signup/',U_views.RegisterView,name = 'signup'),    #For students to sign up
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
