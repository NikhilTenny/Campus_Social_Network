from django.test import TestCase, Client            #Client is used to mimic how users use the views
from django.urls import reverse
from ..models import CustomeUsers,Student_profile
import json


class TestViews(TestCase):

    #Runs before any other test methods
    #Used to setup requirements to carry out tests
    def setUp(self):
        self.client = Client()                              #Create a client instance
        self.home_url = reverse('index')
        self.signup_url = reverse('signup')
        self.signup_data = {
            'username' : 'gon1',
            'first_name' : 'Gon',
            'last_name' : 'Fricks',
            'is_student' : True,
            'password1' : 'fortesting',
            'password2' : 'fortesting',
            'department' : 'bam',
            'year' : 'first',
            'department' : 'bam',
            'year' : 'first'
        }
       

    #Test the index page view
    def test_homepage_GET(self):       
        response = self.client.get(self.home_url)           #Return the response for the get request made to the view through url
        self.assertEquals(response.status_code, 200)        #test if the response for the get request is 200 i.e, success
        self.assertTemplateUsed(response,'core/index.html') #test if the template used id the specified one

    #Test the signup view
    def test_signup_Get(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'users/signup.html')


    def test_signup_Post_creating_student(self):
        response = self.client.post(self.signup_url,self.signup_data)   #Making a post request with data for signup
        self.assertEquals(response.status_code, 302)                    #If successfull signuped in the view it is redirected
                                                                        #Redirect status cod is 302
        
        user = CustomeUsers.objects.all()
        profile = Student_profile.objects.all()
        #For testing a temp db is created with zero records
        self.assertEquals(user.count(),1)                        #if count of user is 1 then it means a user is added successfully                                        
        self.assertEquals(profile.count(),1)


            