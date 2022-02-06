from django.test import TestCase      #This is used in test with no interaction with database 
from django.urls import reverse,resolve     
from ..views import HomeView,RegisterView        
 
#Django looks for tests by first looking for files starting with 'Tests'
#Second, class starting with 'Tests' and third it looks for functions with starting as 'Tests

class TestUrls(TestCase):
    #Test the index page
    def test_home_url(self):
        url = reverse('index')                  #Map the name of url to the url
        #Checks wheater the function(view) of the url is equeal to 'HomeView'
        self.assertEquals(resolve(url).func, HomeView)  #Resolve function get the details related to the url like func(view) arguments...
    
    #Test signup view
    def test_signup_url(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, RegisterView)    