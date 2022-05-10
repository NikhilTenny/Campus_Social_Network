from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic import (TemplateView, ListView, 
        DetailView, UpdateView, 
        DeleteView, CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from chat.models import ChatSpace
from core.models import Posts
from django.contrib import messages
from users.models import CustomeUsers,Profile
from .forms import (
    PostEditForm, RegisterStudentProfileForm,
    RegisterCustomeUserForm, RegisterTeacherProfileForm
    )
from core.forms import notice    
from django.contrib.auth.hashers import make_password


# Admin Dashboard View
class AdminHome(TemplateView, LoginRequiredMixin):
    template_name = 'Admin_area/dashboard.html'
    context_object_name = 'details'
    def get_context_data(self,**kwargs):
        context = {}
        context['posts'] = Posts.objects.all()                  # Most recent posts 
        teachers = list(CustomeUsers.get_Teachers())       # Teachers    
        profiles = list(Profile.objects.filter(User__in=teachers))
        context['teachers'] = zip(teachers,profiles)
        context['totalPosts'] = Posts.objects.all().count()         # Total number of posts
        context['totalUsers'] = ( len(teachers) +             # Total users   
                                  CustomeUsers.get_Students().count() )     # Sum of teachers and students
        return context

# List all the notice board posts
class NoticeBoardView(ListView, LoginRequiredMixin):
    model = Posts
    template_name = 'Admin_area/postlist.html'
    def get_context_data(self):
        context = {}
        context['posts'] = Posts.get_Notice()       # Get all the notice board posts
        context['page_heading'] = 'Notice Board Posts'
        return context

# List all the timeline posts
class TimelineView(ListView, LoginRequiredMixin):
    model = Posts
    template_name = 'Admin_area/postlist.html'
    def get_context_data(self):
        context = {}
        context['posts'] = Posts.get_Timeline()     # Get all the Timeline posts
        context['page_heading'] = 'Timeline Posts'
        return context

# List all the Placement posts
class PlacementView(ListView, LoginRequiredMixin):
    model = Posts
    template_name = 'Admin_area/postlist.html'
    def get_context_data(self):
        context = {}
        context['posts'] = Posts.get_Placement()     # Get all the Timeline posts
        context['page_heading'] = 'Placement Posts'
        return context

# View a Post in detail
class PostDetailView(DetailView, LoginRequiredMixin):
    model = Posts
    template_name = 'Admin_area/postview.html' 
    context_object_name = 'post'

# Edit a post
class PostEditView(UpdateView, LoginRequiredMixin):
    model = Posts 
    template_name = 'Admin_area/postedit.html'  
    form_class = PostEditForm 
        
    def get_context_data(self, *args, **kwargs):
        # Get the context that is already set by the class based view
        context = super(PostEditView, self).get_context_data(*args, **kwargs)
        context['page_heading'] = 'Edit Post'
        return context

    # To redirect to post view page after saving the edited post
    def get_success_url(self):
        viewname = 'adminpostview'
        return reverse(viewname, kwargs ={'slug':self.object.slug})

# View to Remove a post
class PostDeleteView(DeleteView, LoginRequiredMixin, SuccessMessageMixin):
    model = Posts
    success_message = "Post Deleted Successfully"
    #To specify the url to specify after successfull deletion of the post
    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('admin-dashboard')
    def delete(self, request, *args, **kwargs):
        
        return super(PostDeleteView, self).delete(request, *args, **kwargs)    

# View to Register a student
def StudentCreateview(request):
    if request.method == 'POST':
        userForm = RegisterCustomeUserForm(request.POST)
        profileForm = RegisterStudentProfileForm(request.POST) 
        if userForm.is_valid() and profileForm.is_valid():
            passw = make_password('fortesting')   # Making hash of password
            # Getting an instance of the user, but this is not committed to the database
            userObj = userForm.save(False)        
            userObj.password = passw
            userObj.is_student = True
            userObj.save()
            profileObj = profileForm.save(False)
            profileObj.User = userObj
            profileObj.save()
            messages.success(request, "Student Registration Successful")
            return redirect('admin-dashboard')
    # If not a post request then return the page with blank form            
    userForm = RegisterCustomeUserForm()
    profileForm = RegisterStudentProfileForm()
    context = {
        'uform': userForm,
        'pform': profileForm
    }   
    return render(request,'Admin_area/stureg.html',context)

# To register a Teacher
def TeacherCreateView(request):
    if request.method == 'POST':
        userForm = RegisterCustomeUserForm(request.POST)
        profileForm = RegisterTeacherProfileForm(request.POST) 
        if userForm.is_valid() and profileForm.is_valid():
            passw = make_password('fortesting')   # Making hash of password
            # Getting an instance of the user, but this is not committed to the database
            userObj = userForm.save(False)        
            userObj.password = passw
            userObj.is_teacher = True
            userObj.save()
            profileObj = profileForm.save(False)
            profileObj.User = userObj
            profileObj.save()
            return redirect('admin-dashboard')
    # If not a post request then return the page with blank form            
    userForm = RegisterCustomeUserForm()
    profileForm = RegisterTeacherProfileForm()
    context = {
        'uform': userForm,
        'pform': profileForm
    }   
    return render(request,'Admin_area/teacherreg.html',context)

# Show the list of all students    
class StudentListView(ListView, LoginRequiredMixin):
    model = CustomeUsers
    template_name = 'Admin_area/userlist.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        students = list(CustomeUsers.get_Students())    # Getting all the students
        # Getting profiles of the students
        t_profiles = list(Profile.objects.filter(User__in=students))    
        context['Users'] = zip(students, t_profiles)  
        context['heading'] = "Students List"
        # This variable is used to identity that this is a 
        # student list in the template
        context['Student'] = True               
        return context 

# Show the list of all students    
class TeacherListView(ListView, LoginRequiredMixin):
    model = CustomeUsers
    template_name = 'Admin_area/userlist.html'
 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        teachers = list(CustomeUsers.get_Teachers())
        t_profiles = list(Profile.objects.filter(User__in=teachers))
        context['Users'] = zip(teachers, t_profiles)  
        context['heading'] = "Teacher List"
        return context 

# Delete a user(Student/Teacher)
def UserDeleteView(request, username):
    userInst = CustomeUsers.objects.get(username=username)
    userInst.delete()
    return redirect('admin-dashboard')

# Create a Notice board post
class CreateNoticeView(CreateView, LoginRequiredMixin):
    model = Posts
    form_class = notice
    template_name = 'admin_area/createpost.html'

    def get_context_data(self,*args, **kwargs):
        context = super(CreateNoticeView,self).get_context_data(*args, **kwargs)
        # This is displayed in the template as a heading
        context['page_heading'] = 'Notice Board'
        return context

    def form_valid(self,form):
        # Setting the author of the post as the loggined user
        form.instance.Author = self.request.user  
        form.instance.is_notice = True          
        form.instance.is_p_cell = False
        form.instance.is_timeline = False
        return super().form_valid(form)   

# Create a Placement post
class CreatePlacementView(CreateView, LoginRequiredMixin):
    model = Posts
    form_class = notice
    template_name = 'admin_area/createpost.html'

    def get_context_data(self,*args, **kwargs):
        context = super(CreatePlacementView,self).get_context_data(*args, **kwargs)
        context['page_heading'] = 'Placement Cell'
        return context

    def get_success_url(self):
        return  reverse('admin-PM')   

    def form_valid(self,form):
        # Setting the author of the post as the loggined user
        form.instance.Author = self.request.user  
        form.instance.is_notice = False          
        form.instance.is_p_cell = True
        form.instance.is_timeline = False
        return super().form_valid(form)  

# List all discussion rooms
class Dis_roomsView(ListView, LoginRequiredMixin):
    model = ChatSpace
    template_name = 'Admin_area/dis_rooms.html'
    def get_context_data(self, **kwargs):
        rooms = ChatSpace.objects.filter(type='chatroom')
        context = {
            'rooms':rooms,
            'page_heading': 'Discussion Rooms',
        }
        return context


#Edit Discussion room
def EditDis_roomView(request, id):
    roomobj = ChatSpace.objects.get(id=id)
    admin = roomobj.admin.username
    members = roomobj.users.all()
    context = {
        'page_heading':'Edit Discussion Room',
        'room':roomobj,
        'members': members,
        'admin':admin,
    }
    if request.method == 'POST':
        roomobj.description = request.POST['roomdesc']
        roomobj.name = request.POST['roomname']
        roomobj.save()
        messages.success(request, "Details updated")
    return render(request, 'Admin_area/Dis_room_edit.html', context)

# Remove a member from discussion room
def RemMemberView(request, id, username):
    roomobj = ChatSpace.objects.get(id=id)
    user = CustomeUsers.objects.get(username=username)
    roomobj.users.remove(user)
    roomobj.save()
    messages.warning(request, "Member Removed")
    return redirect('admin_edit_dis_room', id)

# list users to add to discussion room
def AddMemberlist(request, id):
    roomobj = ChatSpace.objects.get(id=id)  
    members = ChatSpace.objects.get_members_not_in_room(id)
    context = {
        'room': roomobj,
        'members':members,
       'page_heading':'Add Members to Room',
    }
    return render(request, 'Admin_area/MemberList.html', context)

#Add a user to discussion room
def AddMemberView(request, id, username):
    roomobj = ChatSpace.objects.get(id=id)
    new_member = CustomeUsers.objects.get(username=username) 
    roomobj.users.add(new_member)
    roomobj.save()
    messages.success(request, "New Member Added")
    return redirect('admin_dis_rooms')

# Remove a discussion room
def RemoveRoomView(request, id):
    room = ChatSpace.objects.get(id=id)
    room.delete()
    messages.success(request, "Discussion Room Removed")    
    return redirect('admin_dis_rooms')

# Admin Profile View
def AdminProfileView(request, id):
    admin = CustomeUsers.objects.get(id=id)
    context = {
        'admin':admin,
        'page_heading': 'Profile'
    }
    return render(request, 'Admin_area/AdminProfile.html', context)

# Edit Admin profile 
def EditAdminProfileView(request, id):
    admin = CustomeUsers.objects.get(id=id)
    if request.method == "POST":
        admin.first_name = request.POST['fname']
        admin.last_name = request.POST['lname']
        admin.username = request.POST['uname']
        admin.save()
        messages.success(request, "Profile Successfully Updated")
        return redirect('adminprofile', id)
    return render(request, 'Admin_area/AdminProfileEdit.html')

