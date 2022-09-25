from ast import arg
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomeUsers, Profile
from django.contrib.auth.hashers import make_password
from Admin_area.forms import (RegisterCustomeUserForm,
    RegisterStudentProfileForm,
    RegisterTeacherProfileForm,
    PostEditForm
    )

class TestAdminListViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.admin_details = {
            'username' : 'adminuser',
            'password' : cls.pswd_hash,
            'is_superuser' : 'True'
        }
        cls.ad_user = CustomeUsers.objects.create(**cls.admin_details)
        cls.ad_credentials = {
            'username' : 'adminuser',
            'password' : 'fortesting'
        }

    def test_ad_home_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('admin-dashboard')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/dashboard.html')
    
    def test_notice_board_view_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('admin-NB')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/postlist.html')

    def test_TimelineView_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('admin-TL')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/postlist.html')
    
    def test_PlacementView_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('admin-PM')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/postlist.html')

    def test_StudentListView_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('stulist')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/userlist.html')

    def test_TeacherListView_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('teacherlist')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/userlist.html')

    def test_Dis_roomsView_get(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        self.url = reverse('admin_dis_rooms')

        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response, 'Admin_area/dis_rooms.html')

class TestStudentCreateview(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.admin_details = {
            'username' : 'adminuser',
            'password' : cls.pswd_hash,
            'is_superuser' : 'True'
        }
        cls.ad_user = CustomeUsers.objects.create(**cls.admin_details)
        cls.ad_credentials = {
            'username' : 'adminuser',
            'password' : 'fortesting'
        }
        cls.url = reverse('sturegister')
        cls.form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Yr' : 'first'
        }
    
    def test_StudentCreateview_GET(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.get(self.url)

        self.assertTrue(response.context['uform'])
        self.assertTrue(response.context['pform'])
        self.assertTemplateUsed(response, 'Admin_area/stureg.html')
        self.assertEquals(response.status_code, 200)

    def test_StudentCreateview_POST(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.post(self.url, self.form_data)
        self.created_stu = CustomeUsers.objects.get(username='testuser') 
        
        self.assertTrue(self.created_stu.username, 'testuser')
        self.assertTrue(Profile.objects.get(User=self.created_stu).User, self.created_stu )

        self.assertEquals(response.status_code, 302)

class TestTeacherCreateview(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.admin_details = {
            'username' : 'adminuser',
            'password' : cls.pswd_hash,
            'is_superuser' : 'True'
        }
        cls.ad_user = CustomeUsers.objects.create(**cls.admin_details)
        cls.ad_credentials = {
            'username' : 'adminuser',
            'password' : 'fortesting'
        }
        cls.url = reverse('teacherregister')
        cls.form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Designation' : 'A very good position'
        }
    def test_TeacherCreateView_GET(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.get(self.url)

        self.assertTrue(response.context['uform'])
        self.assertTrue(response.context['pform'])
        self.assertTemplateUsed(response, 'Admin_area/teacherreg.html')
        self.assertEquals(response.status_code, 200)

    def test_TeacherCreateview_POST(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.post(self.url, self.form_data)
        self.created_teacher = CustomeUsers.objects.get(username = 'testuser') 

        
        self.assertTrue(self.created_teacher.username, 'testuser')
        self.assertTrue(Profile.objects.get(User=self.created_teacher).User, self.created_teacher )
        self.assertEquals(response.status_code, 302)

class TestUserDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.admin_details = {
            'username' : 'adminuser',
            'password' : cls.pswd_hash,
            'is_superuser' : 'True'
        }
        cls.ad_user = CustomeUsers.objects.create(**cls.admin_details)
        cls.ad_credentials = {
            'username' : 'adminuser',
            'password' : 'fortesting'
        }
        cls.reg_url = reverse('teacherregister')
        cls.delete_url = reverse('userdelete', args=['testuser'])
        cls.user_form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Designation' : 'A very good position'
        }
        cls.client.post(cls.reg_url, cls.user_form_data)

    def test_UserDeleteView(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        create_response = self.client.post(reverse('teacherregister'), self.user_form_data)
        response = self.client.get(self.delete_url)

        self.assertEquals(response.status_code, 302)

class TestCreateNoticeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.admin_details = {
            'username' : 'adminuser',
            'password' : cls.pswd_hash,
            'is_superuser' : 'True'
        }
        cls.ad_user = CustomeUsers.objects.create(**cls.admin_details)
        cls.ad_credentials = {
            'username' : 'adminuser',
            'password' : 'fortesting'
        }
        cls.notice_form_data = {
            'Title' : 'Hello Title',
            'Content' : 'Hello Title\'s hello content'  
        }
        cls.notice_url = reverse('admincreateNotice')

    def test_CreateNoticeView_GET(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.get(self.notice_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_area/createpost.html')
    

    def test_CreateNoticeView_POST(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.post(self.notice_url, self.notice_form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('admin-NB'))

class TestCreatePlacementView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.admin_details = {
            'username' : 'adminuser',
            'password' : cls.pswd_hash,
            'is_superuser' : 'True'
        }
        cls.ad_user = CustomeUsers.objects.create(**cls.admin_details)
        cls.ad_credentials = {
            'username' : 'adminuser',
            'password' : 'fortesting'
        }
        cls.notice_form_data = {
            'Title' : 'Hello Title',
            'Content' : 'Hello Title\'s hello content'  
        }
        cls.placemnt_url = reverse('admincreatePlacement')

    def test_CreatePlacementView_GET(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.get(self.placemnt_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_area/createpost.html')

    def test_CreatePlacementView_POST(self):
        self.login_response = self.client.post(self.login_url, self.ad_credentials, follow=True)
        response = self.client.post(self.placemnt_url, self.notice_form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('admin-PM'))










