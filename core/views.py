
from typing import List
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Posts, Friends, FriendRequest
from .forms import (
    UserEditForm,
    ProfileEditForm,
    notice   
)
from django.contrib import messages
from users.models import CustomeUsers, Profile
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



# Home page of user
@login_required
def home(request):
    profile = Profile(User=request.user) 
    context = {
        'posts':Posts.objects.filter(is_timeline = True).order_by('-created'), # List of posts that is to be displayed in the user home page
        'notice_post':Posts.objects.filter(is_notice = True).order_by('-created')[:6],
        'p_data':profile,
        }
    return render(request,'core/home.html',context)

# Profile page of the user
@login_required
def ProfileView(request,username): 
    user = CustomeUsers.objects.get(username=username)
    p_data = get_object_or_404(Profile,User=user) 
    friends = Friends.objects.get_friends(request.user)
    frd_list = []
    frd_prof_list = []
    # Get the list of friends of the user from the friends relationship model
    for frd in friends:
        if frd.user1 == request.user:
            frd_list.append(frd.user2)
        else:
            frd_list.append(frd.user1)   
        # Get the profile of the friend             
        prof = Profile.objects.get(
            User=frd_list[-1]
        )
        frd_prof_list.append(prof)
    friend_and_profile = zip(frd_list, frd_prof_list)   
    # Checking whether the logged user and visited profiles user are already friends  
    if_friend = Friends.objects.find_if_friends(user, request.user)
    if if_friend.exists():
        if_friend = True
    context = {
        # List of timeline posts of the logged in user in the descending order of created date
        'posts':Posts.objects.filter(Author=user).filter(is_timeline=True).order_by('-created'),
        'profile':p_data,
        'user_obj':user,
        'fp':friend_and_profile,
        'f_count':len(frd_list),
        'if_friend':if_friend  
        }
    if request.user == user:
        context['edit'] = True
    return render(request,'core/profile.html', context) 

# View to send friend request
@login_required
def FriendRequestView(request, username):
    sender = CustomeUsers.objects.get(username=request.user.username)
    receiver = CustomeUsers.objects.get(username=username)
    # Checking for already existing requests
    req = FriendRequest.objects.filter(
        reqsender=sender, 
        reqreceiver=receiver, 
        rejected=False,
        accepted=False
        
        )
    if req.exists():
        msg = "Friend Request Already Send"
        messages.warning(request,msg)
        return redirect('userprofile',username)
    # If request doesn't exist then a new request is created        
    req = FriendRequest.objects.create(
        reqsender=sender,
        reqreceiver=receiver
    )
    msg = "Friend Request Send"
    messages.success(request,msg)
    return redirect('userprofile',username)

#View to show all the friend requests
class RequestlistView(LoginRequiredMixin, ListView):
    model = FriendRequest
    template_name = 'core/requestlist.html'

    def get_context_data(self, **kwargs):
        context ={}
        context['reqs'] = list(FriendRequest.objects.filter(
            reqreceiver=self.request.user,
            accepted=False,
            pending=True,
            rejected=False, ))
        return context

# Accept a friend request
def AcceptRequest(request, id):
    req = FriendRequest.objects.get(id=id)
    sender = req.reqsender
    req.accepted = True
    req.pending = False
    req.rejected = False
    req.save()
    frdrelation = Friends.objects.create(
        user1=sender,
        user2=request.user
    )
    # Updating the number of friends in both user profile
    Profile.update_friend_no(frdrelation.user1)
    Profile.update_friend_no(frdrelation.user2)

    msg = 'Friend request accepted'
    messages.success(request, msg)
    return redirect('requestlist')

# Reject a friend request
def DeclineRequest(request, id):
    req = FriendRequest.objects.get(id=id)
    req.accepted=False
    req.pending=False
    req.rejected=True
    req.save()
    msg = 'Friend request Rejected'
    messages.warning(request, msg)
    return redirect('requestlist')

# Profile edit view
@login_required
def EditProfileView(request, username):   
    # Get a Profile model object with data of the current logged in user
    p_obj = get_object_or_404(Profile, User=request.user.id)
    if request.method == 'POST':      
        # Get the form with data sent by the user
        userform = UserEditForm(request.POST, instance=request.user)
        profileform = ProfileEditForm(request.POST, request.FILES, instance=p_obj)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect('userprofile',username)   
    else:
        # If it is a GET request then setting the forms with already stored data of the user
        userform = UserEditForm(instance=request.user)
        profileform = ProfileEditForm(instance=p_obj)
        context = {
            'userform': userform,
            'profileform': profileform,
            'p_data': p_obj,
        }
    return render(request,'core/profileEdit.html',context)  

# View to create a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts    
    form_class = notice
    # Set the author of the newly create post as the user logged in 
    def form_valid(self,form):
        form.instance.Author = self.request.user  
        return super().form_valid(form)

# A Detailed view of a certain post
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Posts
    context_object_name = 'post'
    def get_context_data(self,*args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        # There is a edit button in the template
        # Only the author of the post and any teacher can edit a post
        # Only the author can delete a post
        # 
        # Check if the the user is the author or a teacher  
        if (self.object.Author == self.request.user) or self.request.user.is_teacher:
            
            context = super(PostDetailView, self).get_context_data(*args, **kwargs)
            context['edit'] = True                      # Edit button will be accesible to the user
            if self.object.Author == self.request.user: 
                context['delete'] = True                # Delete button will be accesible to the user
            return context
        return context    

#View to edit a post 
class PostEditView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts

    form_class = notice
    def form_valid(self,form):
        return super().form_valid(form)
    #check if it is the author of the post or a teacher who is trying to edit the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.Author or self.request.user.is_teacher:
            return True
        return False        

#List all the teachers, this view is available to the students
class TeachersListView(LoginRequiredMixin, ListView):
    model = CustomeUsers
    context_object_name = 'teacher'
    template_name = 'core/userlist.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        teachers = list(CustomeUsers.get_Teachers())
        # Get the profile instances of the users that are teachers
        # __in filters by the instances in the teachers object
        # That is teachers is a list of teachers and __in filters the profile instance 
        # by the users in the teachers list of instance
        t_profiles = Profile.objects.filter(User__in=teachers)
        # Takes the list of teachers and profiles and aggregates it to a tuple 
        context['Users'] = zip(teachers, t_profiles)  
        return context

#List all the teachers, this view is available to the students
class StudentsListView(LoginRequiredMixin, ListView):
    model = CustomeUsers
    context_object_name = 'student'
    template_name = 'core/userlist.html'
 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        students = list(CustomeUsers.get_Students())
        t_profiles = list(Profile.objects.filter(User__in=students))
        context['Users'] = zip(students, t_profiles)  
        return context        

# List all posts in notice board
class NoticeBoardView(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'core/noticeboard.html'
    context_object_name = 'notice'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice'] =Posts.objects.filter(is_notice = True) 
        return context

# List Placement posts 
class PlacementcellView(LoginRequiredMixin, ListView):
    model = Posts
    template_name = 'core/placementcell.html'
    context_object_name = 'placement'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['placement'] =Posts.objects.filter(is_p_cell = True) 
        return context        

# Create a post in Notice board
class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'core/createpost.html'
    form_class = notice

    def form_valid(self, form):
        form.instance.Author = self.request.user
        form.instance.is_notice = True
        form.instance.is_timeline = False
        form.instance.is_p_cell = False
        return super().form_valid(form)  

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posttype'] = 'Notice'
        return context 

# Create a post in Placement Cell
class PlacementCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'core/createpost.html'
    form_class = notice

    def form_valid(self, form):
        form.instance.Author = self.request.user
        form.instance.is_notice = False
        form.instance.is_timeline = False
        form.instance.is_p_cell = True
        return super().form_valid(form)  

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posttype'] = 'Placement Post'
        return context
# Delete a post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Posts
    
    def get_success_url(self):
        return reverse('userhome')


    









