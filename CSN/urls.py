from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from users import views as U_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('',U_views.HomeView,name = 'index'),
    path('login/',U_views.LoginView,name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
    path('password-reset/', 
            auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'),
            name='password_reset'),
    path('password-reset-done/', 
            auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'),
            name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', 
            auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'),
            name='password_reset_confirm'),  
    path('password-reset-complete/', 
            auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'),
            name='password_reset_complete'),              
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

