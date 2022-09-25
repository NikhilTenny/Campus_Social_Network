from django.test import TestCase
from users.models import CustomeUsers, Profile
from django.contrib.auth.hashers import make_password
from PIL import Image
from Admin_area.tests.test_views import TestStudentCreateview



class TestCustomeUsers(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = make_password('fortesting')
        cls.user_details = {
            'username' : 'testuser',
            'is_student' : 'True',
            'first_name': 'Test_f',
            'last_name' : 'Test_l',
            'password' : cls.password
        }
        cls.user = CustomeUsers.objects.create(**cls.user_details) 
        cls.profile_details = {
            'User' : cls.user
        }
        cls.profile = Profile.objects.create(**cls.profile_details) 


    
    def test_delete(self):
        # Delete the user instance, which will also delete the
        # profile instance associated to it
        self.user.delete()

        self.assertEquals(Profile.objects.all().count(), 0)
    
    def test_model_str_method(self):
        self.assertEquals(self.user.__str__(), 'testuser')


class TestProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = make_password('fortesting')
        cls.user_details = {
            'username' : 'testuser',
            'is_student' : 'True',
            'first_name': 'Test_f',
            'last_name' : 'Test_l',
            'password' : cls.password
        }
        cls.user = CustomeUsers.objects.create(**cls.user_details) 
        cls.profile_details = {
            'User' : cls.user
        }
        cls.profile = Profile.objects.create(**cls.profile_details) 

    def test_update_friend_no(self):
        Profile.update_friend_no(self.user)
        update_prof = Profile.objects.get(User=self.user)

        self.assertEquals(update_prof.Friends, 1) 

    def test_image_resolution(self):
        img = Image.open(self.profile.Profile_pic)
        self.assertEquals(img.size,(400,400))
    
    def test_Profile_str_method(self):
        profile_str = str(self.profile)
        user_str = str(self.user) + " Profile"
        self.assertEquals(profile_str, user_str)


