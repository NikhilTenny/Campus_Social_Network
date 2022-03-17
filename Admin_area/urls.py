from django.urls import path,include
from . import views as ad_views
urlpatterns = [
    path('adminpage/',                              # Admin Dashboard
            ad_views.AdminHome.as_view(), 
            name='admin-dashboard' 
        ),
    path('adminpage/NotceBoard',                    # Notice Board post list
            ad_views.NoticeBoardView.as_view(),
            name='admin-NB'),  
    path('adminpage/Timeline',                      # Timeline post list
            ad_views.TimelineView.as_view(),
            name='admin-TL'),  
    path('adminpage/Placement',                     # Placement cell post list
            ad_views.PlacementView.as_view(),
            name='admin-PM'),   
    path('adminpage/<slug:slug>',
            ad_views.PostDetailView.as_view(),
            name='postview'), 
    path('adminpage/<slug:slug>/edit',
            ad_views.PostEditView.as_view(),
            name='postedit'), 
    path('adminpage/<slug:slug>/delete',
            ad_views.PostDeleteView.as_view(),
            name='postdelete'), 
    path('adminpage/create-student/',
            ad_views.StudentCreateview,
            name = 'sturegister'),                                      

]