from dataclasses import fields
from django import forms
from users.models import CustomeUsers, Profile
from .models import Posts

# Form with feilds of CustomeUser model 
class UserEditForm(forms.ModelForm):
    first_name  = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control'                 #Specify the class name of the input element in the template
        }))                                             #Here the bootstrap classname is given
    last_name  = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control'
        }))
    email  = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control'
        }))        
    class Meta:
        model = CustomeUsers
        fields  = ['first_name', 'email', 'last_name']

# Form with feilds of Profile model
class ProfileEditForm(forms.ModelForm):
    Bio = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2, 
        'cols': 30,
        'class':' bg-light form-control'}),
        required=False)
    Address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2, 
        'cols': 30,
        'class':'bg-light form-control'}),
        required=False)

    Designation = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control'
        }),
        required=False)
    Dept = forms.CharField(widget=forms.Select(
        attrs={
        'class':'bg-light form-control',      
        }, choices=Profile.departments ),
        required=False)    
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control'
        }),
        required=False)     
    class Meta:
        model = Profile
        fields = ['Profile_pic','Bio','Designation','Dept','Address','phone_number']


class notice(forms.ModelForm):
    Title = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control'
        }))
    Content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2, 
        'cols': 30,
        'class':'bg-light form-control'}))
    class Meta:
        model = Posts
        fields = ['Title', 'Content']