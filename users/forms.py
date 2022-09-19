from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomeUsers

#Student signup form
class SignupForm(UserCreationForm):
    department = forms.ChoiceField(choices=[        #dropdown menu to select department
        ('bca','BCA'),
        ('bam','B.A Malayalam'),
        ('bcom','B.com'),
        ('mca','MCA'),
        ('mam','M.A Malayalam'),
        ('bcom','B.com')
    ], required=True)
    year = forms.ChoiceField(choices=[
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third')
    ], required=True)

    class Meta:
        model = CustomeUsers
        fields = ['username','email','first_name',
                  'last_name','department','year']


#Student/Teacher login form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',                 #Specify the class name of the input element in the template
        'id':'yourUsername' 
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',                 #Specify the class name of the input element in the template
        'id':'yourPassword' 
        })) 
