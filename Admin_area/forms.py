from django import forms
from core.models import Posts
from users.models import Profile, CustomeUsers



class PostEditForm(forms.ModelForm):
    Title = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'bg-light form-control',
        'id':'floatingName'
        }))
    Content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 7, 
        'cols': 30,
        'class':'bg-light form-control',
        }))
    class Meta:
        model = Posts
        fields = ['Title', 'Content']

# Form to create Student or Teacher
# A modelform of the model 'Customeusers'
class RegisterCustomeUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'placeholder': 'First Name',
        }
    ), required=True) 
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'placeholder': 'Last Name',
        }
    ), required=True)
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'placeholder': 'Email',
        }
    ), required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'floatingName',
            'placeholder': 'Username',
        }
    ), required=True)

    class Meta:
        model = CustomeUsers
        fields = ['first_name', 'last_name', 'email', 'username']

class RegisterStudentProfileForm(forms.ModelForm):
    Dept = forms.CharField(widget=forms.Select(
        choices=Profile.departments,
        attrs = {
            'class': 'form-select',
            'id': 'floatingSelect',
            'aria-label':"State"
        },
        ),initial='bca', required=True)
    Yr = forms.CharField(widget=forms.Select(
        choices=Profile.year,
        attrs = {
            'class': 'form-select',
            'id': 'floatingSelect',
            'aria-label':"State"
        },
        ),initial='first', required=True)    
        

    class Meta:
        model = Profile
        fields = ['Dept', 'Yr']
     