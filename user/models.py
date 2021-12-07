from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
import base64
from django.urls import reverse

def upload_image_path(instance, filename):
    base_name=os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    final_name = f"{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) }{ext}"
    return f"users/profile-image/{final_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to=upload_image_path,default='empty.png')
    location = models.CharField(max_length=30, blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    image_field=models.TextField(null=True,blank=True)

    def get_contact_url(self):
        return reverse('chat:contact',kwargs={'contact_name':self.user.username})

    def __str__(self) :
        return self.user.username

    def return_email(self):
        return self.user.email

    def save(self,*args,**kwargs):
        if not self.image_field:
           ext = self.profile_image.name.split('.')[-1]
           encoded_string=base64.b64encode(self.profile_image.read())
           ch=encoded_string.decode('utf-8')
           self.image_field = f'data:image/{ext};base64,{ch}'
        super().save(*args,**kwargs)

    def save_image_field(self,*args,**kwargs):
        ext = self.profile_image.name.split('.')[-1]
        encoded_string=base64.b64encode(self.profile_image.read())
        ch=encoded_string.decode('utf-8')
        self.image_field = f'data:image/{ext};base64,{ch}'
        super().save(*args,**kwargs)




@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()