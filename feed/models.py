from django.db import models

# Create your models here.

class Post(models.Model):
    text=models.CharField(max_length=240)
    date=models.DateTimeField(auto_now=True)#to show the date to see waen we postd in admin
    
    def __str__(self) : #to chang the name of the post on admin site we use this  func
        return self.text[0:100]