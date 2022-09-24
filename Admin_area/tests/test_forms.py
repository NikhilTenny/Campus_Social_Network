from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomeUsers, Profile
from django.contrib.auth.hashers import make_password
from Admin_area.forms import (
    RegisterCustomeUserForm,
    RegisterStudentProfileForm,
    RegisterTeacherProfileForm,
    PostEditForm
    )

class TestForms(TestCase):
    def setUp(self):
        self.Cust_user_form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com'
        }
        self.Student_profile_form_data = {
            'Dept': 'bca',
            'Yr' : 'first'
        }
        self.Teacher_profile_form_data = {
            'Dept' : 'baenglish',
            'Designation' : 'A very good position'
        }
        self.Post_form_data = {
            'Title' : 'The grand Title',
            'Content' : 'Content for the Grand Title'
        }

    def test_RegisterCustomeUserForm(self):
        self.form = RegisterCustomeUserForm(self.Cust_user_form_data)
        self.assertTrue(self.form.is_valid())

    def test_RegisterStudentProfileForm(self):
        self.form = RegisterStudentProfileForm(self.Student_profile_form_data)
        self.assertTrue(self.form.is_valid())

    def test_RegisterTeacherProfileForm(self):
        self.form = RegisterTeacherProfileForm(self.Teacher_profile_form_data)
        self.assertTrue(self.form.is_valid())

    def test_PostEditForm(self):
        self.form = PostEditForm(self.Post_form_data)
        self.assertTrue(self.form.is_valid())





