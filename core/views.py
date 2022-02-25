from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Posts
from .forms import UserEditForm,ProfileEditForm
from users.models import CustomeUsers, Profile

#Home page of user
@login_required
def home(request):
    profile = Profile(User = request.user)
    context = {
        'posts':Posts.objects.all().order_by('-created'), #List of posts that is to be displayed in the user home page
        'p_data':profile,
        }

    return render(request,'core/home.html',context)

#Profile page of the user
def ProfileView(request): 
    p_data = get_object_or_404(Profile,User = request.user.id) 
    context = {
        #List of timeline posts of the logged in user in the descending order of created date
        'posts':Posts.objects.filter(Author = request.user.id).filter(is_timeline = True).order_by('-created'),
        'profile':p_data, 
        }
    return render(request,'core/profile.html',context) 

#Profile edit view
def EditProfileView(request):   
    #Get a Profile model object with data of the current logged in user
    p_obj = get_object_or_404(Profile,User = request.user.id)
    if request.method == 'POST':      
        #Get the form with data sent by the user
        userform = UserEditForm(request.POST,instance = request.user)
        profileform = ProfileEditForm(request.POST, request.FILES, instance = p_obj)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect('userprofile')  
    else:
        #If it is a GET request then setting the forms with already stored data of the user
        userform = UserEditForm(instance=request.user)
        profileform = ProfileEditForm(instance=p_obj)
        context = {
            'userform': userform,
            'profileform': profileform,
            'p_data': p_obj,
        }
    return render(request,'core/profileEdit.html',context)      