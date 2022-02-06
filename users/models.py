from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import random

# Store authentication details of every user
class CustomeUsers(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    

    def __str__(self):
        return '{}: {}'.format(self.first_name,self.last_name)

    
#Student profile model
class Student_profile(models.Model):
    #choices in the department field
    bca = 'BCA'
    bam = 'B.A Malayalam'
    bcom = 'B.com'
    mca = 'MCA'
    mam = 'M.A Malayalam'
    mcom = 'M.com'
    depts = [
        (bca,'BCA'),
        (bam,'B.A Malayalam'),
        (bcom,'B.com'),
        (mca,'MCA'),
        (mam,'M.A Malayalam'),
        (bcom,'B.com')
    ]
    #choices in the year field
    first = 'First'
    second = 'Second'
    third = 'Third'
    years = [
        (first, 'First'),
        (second, 'Second'),
        (third, 'Third')
    ]
    defaults = ['default.jpg','default_1.jpg','default_2.jpg','default_3.jpg','default_4.jpg',
                'default_5.jpg','default_6.jpg','default_8.jpg','default_7.jpg']
    pic =random.choice(defaults)
    user = models.OneToOneField(CustomeUsers, on_delete=models.CASCADE)
    bio = models.CharField(max_length=400, blank= True)
    department = models.CharField(max_length=32, choices = depts)
    year = models.CharField(max_length=32, choices = years)
    profile_pic = models.ImageField(default = 'default.jpg',upload_to='profile_pic')

    #Set a default profile pic when a profil is saved
    def save(self, *args, **kwargs):
        if self.profile_pic == 'default.jpg':
            defaults = ['default.jpg','default_1.jpg',      #list of default profile pictures
                        'default_2.jpg','default_3.jpg',
                        'default_4.jpg','default_5.jpg',
                        'default_6.jpg','default_8.jpg',
                        'default_7.jpg']
            self.profile_pic =random.choice(defaults)       #choice a random pic from the list for each Student
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 400 or img.width > 400:             
            resize = (400,400)                      
            img.thumbnail(resize)                       #resize the image to with smaller dimensions
            img.save(self.profile_pic.path)

    def __str__(self):
        return f'{self.user.username} Profile'    

    


