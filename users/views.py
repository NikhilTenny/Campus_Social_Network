from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import SignupForm,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib import messages

#Home page
def HomeView(request):
    return render(request,'core/index.html')


#Student/teacher login page
def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(request, username = uname, password = passw)
            if user is not None:
                login(request,user)
                return render(request,'core/home.html')
                
            else:
                form = LoginForm()
                messages.error(request,'username or password not correct')
                return render(request,'users/login.html',{'form':form}) 
    else:
        form = LoginForm()
        return render(request,'users/login.html',{'form':form}) 
