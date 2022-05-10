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
        path('adminpage/list-dis_room/',                # List all the discussion rooms
                ad_views.Dis_roomsView.as_view(),
                name='admin_dis_rooms'
        ),
        path('adminpage/list-dis_room/<int:id>/',       # Edit a discussion room
                ad_views.EditDis_roomView,
                name='admin_edit_dis_room'
        ),
        path('adminpage/list-dis_room/<int:id>/remove/<str:username>',  # Remove a member from a room
                ad_views.RemMemberView,
                name='rem_member'
        ),
        path('adminpage/list-dis_room/<int:id>/addmember',        #List all the user to add to the room
                ad_views.AddMemberlist,
                name='memberstoadd'
        ), 
        path('adminpage/list-dis_room/<int:id>/addmember/<str:username>/add',
                ad_views.AddMemberView,
                name='addmember'
        ),
        path('adminpage/list-dis_room/<int:id>/remove',                # Remove a discussion room
                ad_views.RemoveRoomView,
                name='removeroom'
        ), 
        path('adminpage/profile/<int:id>/',                            # View admin profile
                ad_views.AdminProfileView,
                name='adminprofile'
        ),
        path('adminpage/profile/<int:id>/edit/',                       # Admin profile edit view
                ad_views.EditAdminProfileView,
                name='adminprofileedit'
        )                  
]