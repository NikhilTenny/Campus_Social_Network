from django.test import TestCase
from django.contrib.auth.hashers import make_password
from users.models import CustomeUsers, Profile
from core.models import Friends, Posts, FriendRequest
from django.urls import reverse 

class TestPosts(TestCase):
    def setUp(self):
        
        self.password = make_password('fortesting')
        self.user_details = {
            'username' : 'testuser',
            'is_student' : 'True',
            'first_name': 'Test_f',
            'last_name' : 'Test_l',
            'password' : self.password
        }
        self.user = CustomeUsers.objects.create(**self.user_details) 
        self.post_details = {
            'Author' : self.user,
            'Title' : 'Hello Test Title',
            'is_timeline' : 'True',
        }
        self.slug = 'hello-test-title'
        self.post = Posts.objects.create(**self.post_details) 
            
    def test_slugify(self):
        post_slug = self.post.slug

        self.assertEquals(self.slug, post_slug)
    
    def test_get_notice(self):
        self.post.is_timeline = False
        self.post.is_notice = True
        self.post.save()

        self.assertEquals(Posts.objects.all().first(), Posts.get_Notice().first())

    def test_get_timeline(self):
        self.post.save()
        
        self.assertEquals(Posts.objects.all().first(), Posts.get_Timeline().first())

    def test_get_Placement(self):
        self.post.is_timeline = False
        self.post.is_p_cell = True        
        self.post.save()
        
        self.assertEquals(Posts.objects.all().first(), Posts.get_Placement().first())
    
    def test_str(self):
        title = str(self.post)
        self.assertEquals(title, self.post.Title)

    def test_get_absolute_url(self):
        url = reverse('postdetail', args=[self.slug])
        
        self.assertEquals(url, self.post.get_absolute_url())

class TestFriends(TestCase):
    def setUp(self):
        self.password = make_password('fortesting')
        self.user_details = {
            'username' : 'testuser',
            'is_student' : 'True',
            'first_name': 'Test_f',
            'last_name' : 'Test_l',
            'password' : self.password
        }
        self.user1_details = {
            'username' : 'testuser1',
            'is_student' : 'True',
            'first_name': 'Test_f1',
            'last_name' : 'Test_l1',
            'password' : self.password
        }
        self.user = CustomeUsers.objects.create(**self.user_details)  
        self.user1 = CustomeUsers.objects.create(**self.user1_details)  
        self.friends = Friends.objects.create(user1=self.user, user2=self.user1)

    def test_str(self):
        friends_str = str(self.friends)
        frds = str(self.user) +' and '+str(self.user1)

        self.assertEquals(friends_str, frds)
    
class TestFriendRequest(TestCase):
    def setUp(self):
        self.password = make_password('fortesting')
        self.user_details = {
            'username' : 'testuser',
            'is_student' : 'True',
            'first_name': 'Test_f',
            'last_name' : 'Test_l',
            'password' : self.password
        }
        self.user1_details = {
            'username' : 'testuser1',
            'is_student' : 'True',
            'first_name': 'Test_f1',
            'last_name' : 'Test_l1',
            'password' : self.password
        }
        self.user = CustomeUsers.objects.create(**self.user_details)  
        self.user1 = CustomeUsers.objects.create(**self.user1_details)  
        self.reqs = FriendRequest.objects.create(reqsender =self.user, reqreceiver =self.user1)

    def test_str(self):
        friends_str = str(self.reqs)
        frds = str(self.user) +' to '+str(self.user1)

        self.assertEquals(friends_str, frds)    



        