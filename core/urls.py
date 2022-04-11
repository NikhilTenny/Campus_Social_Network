from django.contrib import admin
from django.urls import path, include
from .views import (
    home, ProfileView, EditProfileView, 
    PostCreateView, PostDetailView, PostEditView,
    TeachersListView, NoticeBoardView, NoticeCreateView,
    PlacementcellView, PlacementCreateView, StudentsListView,
    PostDeleteView, FriendRequestView, RequestlistView,
    AcceptRequest, DeclineRequest   
)
urlpatterns = [
    path('home/',home, name='userhome'),
    path('profile/<username>/', ProfileView, name='userprofile'),                   # View profile of user
    path('profile/<username>/request',                                              # Send a friend request    
        FriendRequestView, 
        name='friendrequest'),    
    path('home/friend-requests', RequestlistView.as_view(), name='requestlist'),    # List all friend requests
    path('home/friend-requests/accept/<int:id>', AcceptRequest, name='acceptrequest'),  # Accept a friend request
    path('home/friend-requests/reject/<int:id>', DeclineRequest, name='rejectrequest'), # Reject a friend request
    path('<username>/editprofile/', EditProfileView, name='editprofile'),           # Edit profile of user
    path('home/createpost', PostCreateView.as_view(), name='createpost'),           # Create a post
    path('home/post/<slug:slug>', PostDetailView.as_view(), name='postdetail'),     # Detail view of a post
    path('home/post/<slug:slug>/edit', PostEditView.as_view(), name='postedit'),    # Edit a post
    path('home/post/<slug:slug>/delete',                                            # Edit a post 
        PostDeleteView.as_view(), 
        name='postdelete'),      
    path('home/teachers', TeachersListView.as_view(), name='teacherslist'),          # List of all teachers
    path('home/students', StudentsListView.as_view(), name='studentslist'),          # List of all students
    path('home/noticeboard', NoticeBoardView.as_view(), name='noticeboard'),        # List all posts in Notice board
    path('home/noticeboard/create',
            NoticeCreateView.as_view(), 
            name='createnotice'),           # Create a notice board post
    path('home/p_cell', 
            PlacementcellView.as_view(), 
            name='placementcell' ),         # List of posts in placement cell
    path('home/p_cell/create',
            PlacementCreateView.as_view(), 
            name='placementcreate'),        # Create a placement post     
]