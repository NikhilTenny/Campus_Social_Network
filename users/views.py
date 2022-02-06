from django.shortcuts import redirect, render
from django.contrib import messages
from users.models import Student_profile
from .forms import SignupForm

#Home page
def HomeView(request):
    return render(request,'core/index.html')


#Student Signup page
def RegisterView(request):
    if request.method == "POST":                #If signup data is send via POST method
        form = SignupForm(request.POST)         
        if form.is_valid():                     #Check if the form data is valid
            user = form.save(False)             #Saving the form without commiting the changes to db. It Return a model(CustomUsers) instance
            user.is_student = True              #Set the student flag of the instance.
            user.save()                         #save the instance to db
            id = user.id
            dept = form.cleaned_data['department']
            yr = form.cleaned_data['year']
            obj = Student_profile(user = user,department = dept,year = yr)  #Create a profile instance with given data
            obj.save()
            return redirect('index')
    else:
        form = SignupForm()
    return render(request,'users/signup.html',{'form':form})
