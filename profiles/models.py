
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    image = ImageField(upload_to='profiles')

    def __str__(self) : #to chang the name of the post on admin site we use this  func
        return self.user.username
    
@receiver(post_save, sender=User)     
def creat_user_profile(sender,instance,created,**kwargs):
    #create a new profile objact when a django user is created
    if created:
        Profile.objects.create(user=instance)