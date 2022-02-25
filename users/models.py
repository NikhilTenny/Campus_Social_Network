from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import random
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


# Store authentication details of every user
class CustomeUsers(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def save(self,*args,**kwargs):
        #checking whether there exist a profile for the user
        try:    
            p_count = Profile.objects.get(User = self.id)
        except:    
            p_count = False
        #If there is no profile for the user create one. This happens at the time of registration 
        if  not p_count:
            self.password = make_password(self.password)        #Hashing the password before storing
            #Create a new Profile instance associated with the registered user
            p_obj = Profile()
            p_obj.User = self
            super().save(*args,**kwargs)
            p_obj.save()
        else:
            super().save(*args,**kwargs)

            
  
        
                        

    def __str__(self):
        return self.username

user  = get_user_model()
#Profile details of a teacher or student
class Profile(models.Model):
    departments = (
        ('bca','BCA'),
        ('bamalayalam','B.A Malayalam'),
        ('baenglish','B.A English'),
        ('bscchemistry','BSC Chemistry'),
    )
    year = (
        ('first','First'),
        ('second','Second'),
        ('third','Third'),
    )
    Bio = models.CharField(max_length=400, blank=True)
    Dept = models.CharField(max_length=30,choices=departments, blank=True)
    Yr = models.CharField(max_length=30,choices=year, blank=True)
    User = models.OneToOneField(user, on_delete=models.CASCADE)
    Profile_pic = models.ImageField(default='default.jpg',upload_to='profile_pic')
    phone_regex = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) #phone number field with validations
    Designation = models.CharField(max_length=50, blank=True)
    Address = models.CharField(max_length=300, blank=True)
    Friends = models.CharField(max_length=50, default = 0)
    Posts = models.CharField(max_length=50, default = 0)
    

    #Set a default profile pic when a profil is saved
    def save(self, *args, **kwargs):
        if self.Profile_pic == 'default.jpg':
            defaults = ['default_1.jpg',                #list of default profile pictures
                        'default_2.jpg','default_3.jpg',
                        'default_4.jpg','default_5.jpg',
                        'default_6.jpg','default_8.jpg',
                        'default_7.jpg']
            self.Profile_pic =random.choice(defaults)       #choice a random pic from the list for each Student
           
        super().save(*args, **kwargs)
        img = Image.open(self.Profile_pic.path)
        if img.height > 400 or img.width > 400:             
            resize = (400,400)                      
            img.thumbnail(resize)                           #resize the image to with smaller dimensions
            img.save(self.Profile_pic.path)

    def __str__(self):
        return f'{self.User.username} Profile' 
           

    


