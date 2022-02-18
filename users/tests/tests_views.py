from django.test import TestCase, Client            #Client is used to mimic how users use the views
from django.urls import reverse
from ..models import CustomeUsers,Student_profile
import json


class TestViews(TestCase):  

    #Test the index page view
    def test_homepage_GET(self):       
        response = self.client.get(self.home_url)           #Return the response for the get request made to the view through url
        self.assertEquals(response.status_code, 200)        #test if the response for the get request is 200 i.e, success
        self.assertTemplateUsed(response,'core/index.html') #test if the template used id the specified one






            