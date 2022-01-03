from django.db import models
from django.urls import reverse
import os
import random
import string
from extensions.utils import jalali_date_time_converter
from user.models import Profile


def upload_image_path(instance, filename):
    base_name=os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    final_name = f"{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) }{ext}"
    return f"users/profile-image/{final_name}"


class Chat(models.Model):
    author=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='author')
    roomname= models.CharField(max_length=100)
    profile=models.ImageField(upload_to=upload_image_path,default='group.png')
    members= models.ManyToManyField(Profile,related_name='members')
    label=models.CharField(max_length=8)

    def __str__(self):
        return self.roomname

    def get_absolute_url(self):
        return reverse('chat:room',kwargs={'room_name':self.roomname.replace(' ', '-')})


    def delete_chat_url(self):
        return reverse('chat:delete',kwargs={'room_name':self.roomname.replace(' ', '-')})
    
    def get_last_message(self):
        return self.message_set.all().last()
    

class Message (models.Model):
   author = models.ForeignKey(Profile,on_delete=models.CASCADE)
   message= models.TextField()
   related_chat=models.ForeignKey(Chat,on_delete=models.CASCADE)
   timestamp= models.DateTimeField(auto_now_add=True)
   label=models.CharField(max_length=10)
   def __str__(self):
       return self.author.user.username

   def local_date(self):
        return jalali_date_time_converter(self.timestamp)

   local_date.short_description='date'

   def get_message(self):
       if len(self.message)>40:
        return f'{self.message[:40]} ...'
       else:
           return self.message

   get_message.short_description='message'

   def get_author_chat(self):
       return Chat.objects.filter(members=self.author).all

   
#    def get_related_chat(self,request,**kwargs):
#        if self.related_chat.label=='contact':
#            return f'{request} {kwargs}'
#        else:
#            return self.related_chat


   def get_user_profile(self):
       return self.author.image_field

   def all_message(self,roomname):
       return Message.objects.filter(related_chat__roomname = roomname).order_by('-timestamp')

   def last_message(self):
       room=Message.objects.last().related_chat
       return room

