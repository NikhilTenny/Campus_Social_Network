from django.urls import path,include
from . import views as ad_views

urlpatterns = [
        path('adminpage/',                              # Admin Dashboard
                ad_views.AdminHome.as_view(), 
                name='admin-dashboard'),
        path('adminpage/NotceBoard',                    # Notice Board post list
                ad_views.NoticeBoardView.as_view(),
                name='admin-NB'),  
        path('adminpage/Timeline',                      # Timeline post list
                ad_views.TimelineView.as_view(),
                name='admin-TL'),  
        path('adminpage/Placement',                     # Placement cell post list
                ad_views.PlacementView.as_view(),
                name='admin-PM'),   
        path('adminpage/<slug:slug>',                   # Detailed view of a post
                ad_views.PostDetailView.as_view(),
                name='adminpostview'), 
        path('adminpage/<slug:slug>/edit',              # Edit a post
                ad_views.PostEditView.as_view(),
                name='adminpostedit'), 
        path('adminpage/<slug:slug>/delete',            # Delete a post
                ad_views.PostDeleteView.as_view(),
                name='adminpostdelete'), 
        path('adminpage/create-student/',               # Register a student
                ad_views.StudentCreateview,
                name = 'sturegister'),  
        path('adminpage/create-teacher/',               # Register a teacher    
                ad_views.TeacherCreateView,
                name = 'teacherregister'),                                                    
        path('adminpage/student-list/',                 # Show the list of students
            ad_views.StudentListView.as_view(),
            name='stulist'),   
        path('adminpage/teacher-list/',                 # Show the list of students
            ad_views.TeacherListView.as_view(),
            name='teacherlist'),
        path('adminpage/<username>/userdelete',         # Delete a user    
                ad_views.UserDeleteView,
                name = 'userdelete'),
        path('adminpage/create-notice/',                # Create a Notice board post
            ad_views.CreateNoticeView.as_view(),
            name='admincreateNotice'),   
        path('adminpage/create-placement/',             # Create a Placement cell post
            ad_views.CreatePlacementView.as_view(),
            name='admincreatePlacement'),                       
]