from django.test import TestCase
from users.models import CustomeUsers, Profile
from django.contrib.auth.hashers import make_password
from PIL import Image



class TestCustomeUsers(TestCase):
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
        self.profile_details = {
            'User' : self.user
        }
        self.profile = Profile.objects.create(**self.profile_details) 


    
    def test_delete(self):
        # Delete the user instance, which will also delete the
        # profile instance associated to it
        self.user.delete()

        self.assertEquals(Profile.objects.all().count(), 0)
    
    def test_model_str_method(self):
        self.assertEquals(self.user.__str__(), 'testuser')


class TestProfile(TestCase):
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
        self.profile_details = {
            'User' : self.user
        }
        self.profile = Profile.objects.create(**self.profile_details) 

    # def test_update_friend_no(self):
    #     Profile.update_friend_no(self.user)

    #     print(self.profile.Friends)
    #     self.assertEquals(self.profile.Friends, 1) 

    def test_image_resolution(self):
        img = Image.open(self.profile.Profile_pic)
        self.assertEquals(img.size,(400,400))
    
    def test_Profile_str_method(self):
        profile_str = str(self.profile)
        user_str = str(self.user) + " Profile"
        self.assertEquals(profile_str, user_str)


