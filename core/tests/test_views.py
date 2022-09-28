from ast import arg
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from core.models import FriendRequest, Friends, Posts
from users.models import CustomeUsers, Profile
from django.contrib.auth.hashers import make_password

class TestProfileAndFriendRequestView(TestCase):

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
        cls.user_form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Yr' : 'first'
        }
        cls.user1_form_data = {
            'first_name' : 'test_f_name1',
            'last_name' : 'test_l_name1',
            'username' : 'testuser1',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Yr' : 'first'
        }
        cls.user_credentials = {
            'username' : 'testuser',
            'password' : 'fortesting'
        }
        cls.login_response = cls.client.post(cls.login_url, cls.ad_credentials, follow=True)
        cls.create_url = reverse('sturegister') 
        # Register 2 users
        cls.stu_create_response = cls.client.post(cls.create_url, cls.user_form_data)
        cls.stu1_create_response = cls.client.post(cls.create_url, cls.user1_form_data)
          
        cls.profile_url = reverse('userprofile', args=['testuser'])


    
    def test_ProfileView(self):
        # Make them friends
        stu = CustomeUsers.objects.get(username='testuser')
        stu1 = CustomeUsers.objects.get(username='testuser1')
        Friends.objects.create(user1=stu, user2=stu1)
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        
        response = self.client.get(self.profile_url)

        self.assertTemplateUsed(response, 'core/profile.html')
    
    def test_FriendRequestView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('friendrequest', args=['testuser'])

        response = self.client.get(url)

        self.assertEquals(FriendRequest.objects.all().count(), 1)
        self.assertEquals(response.status_code, 302)
    
    def test_FriendRequestView_already_send(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('friendrequest', args=['testuser'])

        response = self.client.get(url)
        response1 = self.client.get(url)


        self.assertEquals(FriendRequest.objects.all().count(), 1)
        self.assertEquals(response1.status_code, 302)
    
    def test_RequestlistView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('requestlist')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/requestlist.html')
    
    def test_AcceptRequest(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        stu = CustomeUsers.objects.get(username='testuser')
        # Sending a friend request
        frd_req_url = reverse('friendrequest', args=['testuser'])
        self.client.get(frd_req_url)
        # Get the id of the request
        frd_req_id = FriendRequest.objects.get(reqsender=stu).id
        url = reverse('acceptrequest', args=[frd_req_id])

        response = self.client.get(url)

        self.assertRedirects(response, reverse('requestlist'))
    
    def test_DeclineRequest(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        stu = CustomeUsers.objects.get(username='testuser')
        # Sending a friend request
        frd_req_url = reverse('friendrequest', args=['testuser'])
        self.client.get(frd_req_url)
        # Get the id of the request
        frd_req_id = FriendRequest.objects.get(reqsender=stu).id
        url = reverse('rejectrequest', args=[frd_req_id])
        
        response = self.client.get(url)

        self.assertRedirects(response, reverse('requestlist'))

class TestProfileEdit(TestCase):
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
        cls.user_form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Yr' : 'first'
        }
        cls.user_credentials = {
            'username' : 'testuser',
            'password' : 'fortesting'
        }

        cls.login_response = cls.client.post(cls.login_url, cls.ad_credentials, follow=True)
        cls.create_url = reverse('sturegister') 
        cls.stu_create_response = cls.client.post(cls.create_url, cls.user_form_data)

    def test_EditProfileView_GET(self):
        url = reverse('editprofile', args=['testuser'])
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profileEdit.html')
    
    def test_EditProfileView_POST(self):
        url = reverse('editprofile', args=['testuser'])
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        self.user_form_data['first_name'] = 'newname'

        response = self.client.post(url, self.user_form_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('userprofile', args=['testuser']))
    
class TestPostViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login')
        cls.pswd_hash = make_password('fortesting')
        cls.user_data = {
            'username' : 'testuser',
            'password' : cls.pswd_hash,
            'is_student' : 'True'
        }
        cls.user_credentials = {
            'username' : 'testuser',
            'password' : 'fortesting'
        }
        cls.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
        }
        cls.user = CustomeUsers.objects.create(**cls.user_data)
        
    
    def test_PostCreateView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('createpost')

        response = self.client.post(url, self.post_data)

        self.assertEquals(response.status_code, 302)
    
    def test_PostDetailView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)     
        #Create a post
        create_url = reverse('createpost')
        post_create_response = self.client.post(create_url, self.post_data)
        slug = Posts.objects.get(Author=self.user).slug
        url = reverse('postdetail', args=[slug])

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_PostEditView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        #Create a post
        create_url = reverse('createpost')
        post_create_response = self.client.post(create_url, self.post_data)
        slug = Posts.objects.get(Author=self.user).slug
        url = reverse('postedit', args=[slug])
        self.post_data['Title'] = 'New Title'

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

class TestListAndDetailView(TestCase):
    
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
        cls.user_form_data = {
            'first_name' : 'test_f_name',
            'last_name' : 'test_l_name',
            'username' : 'testuser',
            'email' : 'test@testdomain.com',
            'Dept': 'bca',
            'Designation' : 'Teacher'
        }
        cls.user_credentials = {
            'username' : 'testuser',
            'password' : 'fortesting'
        }

        cls.login_response = cls.client.post(cls.login_url, cls.ad_credentials, follow=True)
        cls.create_url = reverse('teacherregister') 
        cls.Tr_create_response = cls.client.post(cls.create_url, cls.user_form_data)
        cls.user = CustomeUsers.objects.get(username='testuser')

        
    
    def test_TeacherListView(self):
        url = reverse('teacherslist')
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)     

        response = self.client.get(url)

        self.assertTemplateUsed(response, 'core/userlist.html')
        
    
    def test_StudentListView(self):
        url = reverse('studentslist')
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)    
        # Create a notice
        self.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
            'is_notice' : 'True',
            'Author' : self.user
        }
        Posts.objects.create(**self.post_data) 

        response = self.client.get(url)

        self.assertTemplateUsed(response, 'core/userlist.html')

    def test_PlacementView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        # Create a Placement cell post
        self.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
            'is_p_cell' : 'True',
            'Author' : self.user
        }
        Posts.objects.create(**self.post_data)
        url = reverse('placementcell')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
    
    def test_NoticeBoardView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        # Create a notice
        self.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
            'is_notice' : 'True',
            'Author' : self.user
        }
        Posts.objects.create(**self.post_data)
        url = reverse('noticeboard')

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)


class TestPostCreateViews(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.login_url = reverse('login') 
        cls.pswd_hash = make_password('fortesting')
        cls.user_form_data = {
            'username' : 'testuser',
            'password' : cls.pswd_hash
        }
        cls.user_credentials = {
            'username' : 'testuser',
            'password' : 'fortesting'
        }
        cls.user = CustomeUsers.objects.create(**cls.user_form_data)

    def test_NoticeCreateView_POST(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('createnotice')
        self.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
        }

        response = self.client.post(url, self.post_data)

        self.assertEquals(response.status_code, 302)

    def test_NoticeCreateView_GET(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('createnotice')


        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['posttype'], 'Notice')



    def test_PlacementCreateView_POST(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('placementcreate')
        self.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
        }

        response = self.client.post(url, self.post_data)

        self.assertEquals(response.status_code, 302)

    def test_PlacementCreateView_GET(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        url = reverse('placementcreate')


        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['posttype'], 'Placement Post')
    
    def test_PostDeleteView(self):
        self.login_response = self.client.post(self.login_url, self.user_credentials, follow=True)
        create_url = reverse('placementcreate')
        self.post_data = {
            'Title' : 'A post Title',
            'Content' : 'A post Content',
        }
        create_response = self.client.post(create_url, self.post_data)
        slug = 'a-post-title'
        url = reverse('postdelete', args=[slug])

        response = self.client.post(url)

        self.assertRedirects(response, reverse('userhome'))


        








        













        




    







        
    

