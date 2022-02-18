from dataclasses import fields
from django.contrib import admin
from .models import CustomeUsers,Profile
from django import forms

#This is used to add field of a model to another model with a relationship
# class Student_profileInline(admin.StackedInline):
#     model = Student_profile
#     fields = ['user']


# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = CustomeUsers
#         fields = ['username','first_name','last_name','email','password']

#This class contains the properties of the arragment of fields that
#should appear with CustomeUser model in the admin page
class CustomeUserAdmin(admin.ModelAdmin):           
    fieldsets = (                                                   
        ('Register Student',{
            'fields': ['username','first_name','last_name','email','password','is_student','is_teacher'],
        }),
    )

admin.site.register(Profile)
admin.site.register(CustomeUsers,CustomeUserAdmin)  #'CustomeUserAdmin' is the class with the properties for this model in the admin page

