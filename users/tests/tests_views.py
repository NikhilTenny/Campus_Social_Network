from multiprocessing import context
from pydoc import resolve
from django.test import TestCase, Client            #Client is used to mimic how users use the views
from django.urls import reverse
from users.models import CustomeUsers, Profile
from core.models import Posts
from django.contrib.auth.hashers import make_password
import json

class TestLoginView(TestCase):

    def setUp(self):
        self.url = reverse('login')
        self.client = Client()
        self.password = make_password('fortesting')
        self.user_details = {
            'username' : 'testuser',
            'is_student' : 'True',
            'first_name': 'Test_f',
            'last_name' : 'Test_l',
            'password' : self.password
        }
        self.login_credentials = {
            'username' : 'testuser',
            'password' : 'fortesting'
        }
        self.user = CustomeUsers.objects.create(**self.user_details) 


    def test_login_GET(self):
        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_POST_valid(self):
        response = self.client.post(self.url, self.login_credentials, follow=True)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')


    def test_login_POST_super_user(self):
        self.user.is_student = False
        self.user.is_superuser = True
        self.user.save()

        response = self.client.post(self.url, self.login_credentials, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Admin_area/dashboard.html')

    def test_login_POST_invalid(self):
        self.login_credentials['password'] = 'invalid_pass'
        response = self.client.post(self.url, self.login_credentials, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')







 







            