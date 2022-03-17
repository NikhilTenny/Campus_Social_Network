from msilib.schema import ListView
from pipes import Template
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from core.models import Posts
from users.models import CustomeUsers,Profile
from .forms import PostEditForm, RegisterStudentProfileForm, RegisterCustomeUserForm
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
        viewname = 'postview'
        return reverse(viewname, kwargs ={'slug':self.object.slug})

# View to Remove a post
class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Posts
    
    #To specify the url to specify after successfull deletion of the post
    def get_success_url(self):
        return reverse('admin-dashboard')

def StudentCreateview(request):
    if request.method == 'POST':
        userForm = RegisterCustomeUserForm(request.POST)
        profileForm = RegisterStudentProfileForm(request.POST) 
        if userForm.is_valid() and profileForm.is_valid():
            passw = make_password('fortesting')   # Making hash of password
            userObj = userForm.save(False)
            userObj.password = passw
            userObj.is_student = True
            userObj.save()
            profileObj = profileForm.save(False)
            profileObj.User = userObj
            profileObj.save()
            return redirect('admin-dashboard')
    userForm = RegisterCustomeUserForm()
    profileForm = RegisterStudentProfileForm()
    context = {
        'uform': userForm,
        'pform': profileForm
    }    

    return render(request,'Admin_area/stureg.html',context)

    


