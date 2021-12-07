from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from .models import Chat,Message
from user.models import Profile
from .serializers import MessageSerializer,OnlineUserSerializer
from rest_framework.renderers import JSONRenderer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import base64

online_members=[]
 


class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name=f'chat_{self.room_name}'  
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
        if self.room_name!='listener' and self.room_name!='onlineUser':
            await self.onlineUser(self.room_name)
    
    async def onlineUser(self,roomname):
        members_list=await self.get_chat_online_members(roomname)
        members_json=await self.serializers(OnlineUserSerializer,members_list,True)
        await self.channel_layer.group_send(
            'chat_onlineUser',
            {
                'type':'chat_message',
                'members_list':members_json,
                
            }
        )
        
   

    @database_sync_to_async
    def get_user_profile(self,profile_image):
       ext = self.profile_image.name.split('.')[-1]
       encoded_string=base64.b64encode(self.profile_image.read())
       ch=encoded_string.decode('utf-8')
       return f'data:image/{ext};base64,{ch}'

    @database_sync_to_async
    def get_chat_online_members(self,roomname):
        chat_model=Chat.objects.get(roomname = roomname)
        members=chat_model.members.all()
        global online_members
        chat_online_members=list(set(members) & set(online_members))
        return chat_online_members
    
  
         
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    @database_sync_to_async
    def serializers(self,serializer,qs,class_name):
        serialized = serializer(qs, many=class_name)
        content = JSONRenderer().render(serialized.data)       
        return eval(content)
    
    @database_sync_to_async
    def get_user_model(self,username):
        return Profile.objects.filter(user__username=username).first()

    @database_sync_to_async
    def get_chat_model(self,roomname):
        return Chat.objects.filter(roomname=roomname).first()

    @database_sync_to_async
    def create_message_model(self,user_model,message,chat_model,label):
        return Message.objects.create(author=user_model,message=message,related_chat=chat_model,label=label)
    
    async def new_message(self,data):
        data['label']='text'
        user_model=await self.get_user_model(data['__str__'])
        chat_model=await self.get_chat_model(data['roomname'])
        message_model= await self.create_message_model(user_model,data['message'],chat_model,'text')
        result=await self.serializers(MessageSerializer,message_model,False)
        result['command']='new_message'
        await self.send_to_chat_message(result)
        data['local_date']=message_model.local_date()
        await self.notif(data)
    
    @database_sync_to_async
    def get_chat_members(self,roomname):
        members = Chat.objects.get(roomname = roomname).members.all()
        members_list=[]
        for _ in members:
            members_list.append(_.user.username)
        
        return members_list
          
    async def notif(self,data):
        members_list=await self.get_chat_members(data['roomname'])        
        await self.channel_layer.group_send(
            'chat_listener',
            {
                'type':'chat_message',
                'message':data['message'],
                'label':data['label'],
                'members_list':members_list,
                'roomname':data['roomname'],
                '__str__':data['__str__'],
                'local_date':data['local_date'],
            }
        )
       
    @database_sync_to_async
    def fetch_message_queries(self,data):
        return Message.all_message(self,data['roomname'])
        
    async def fetch_messages(self,data):
        messages=await self.fetch_message_queries(data)
        message_json=await self.serializers(MessageSerializer,messages,True)
        result={
            'message':message_json,
            'command':'fetch_message'
        }
        await self.chat_message(result)

    async def image(self,data):
        data['label']='image'
        chat_model=await self.get_chat_model(data['roomname'])
        user_model = await self.get_user_model(data['__str__'])
        message_model=await self.create_message_model(user_model,data['message'],chat_model,'image')
        result=await self.serializers(MessageSerializer,message_model,False)
        result['command']='image'
        data['local_date']=message_model.local_date()
        await self.notif(data)
        await self.send_to_chat_message(result)
    
    
    commands={
        'fetch_message':fetch_messages,
        'new_message':new_message,
        'image':image
    }

    
    
    async def receive(self, text_data):
        data=json.loads(text_data)
        command=data['command']
        roomname=data['roomname']
        await self.commands[command](self,data) 
        
        
        
    async def send_to_chat_message(self,data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':data['message'],
                'command':data['command'],
                '__str__':data['__str__'],
                'label':data['label'],
                'local_date':data['local_date'],
                'get_user_profile':data['get_user_profile']
            })

    async def chat_message(self,data):   
        await self.send(text_data=json.dumps(data))


        

class ConnectConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
        await self.update_online_members(self.scope['user'],True)
        

    @database_sync_to_async
    def update_online_members(self,user,status):
        user = Profile.objects.filter(user=user).first()
        global online_members
        if status is True:
            online_members.append(user)
        elif status is False:
            online_members.remove(user)  

        
        
    async def disconnect(self, code):
        await self.update_online_members(self.scope['user'],False)
        
   
    
    




    


# class ChatConsumer(AsyncWebsocketConsumer):
    
#     async def connect(self):
#         self.room_name=self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name=f'chat_{self.room_name}'
#         await self.channel_layer.group_add(self.room_group_name,self.channel_name)
#         await self.accept()
    
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

#     @database_sync_to_async
#     def message_serializers(self,qs,class_name):
#         serialized = MessageSerializer(qs, many=class_name)
#         content = JSONRenderer().render(serialized.data)       
#         return eval(content)
    
#     @database_sync_to_async
#     def get_user_model(self,username):
#         return Profile.objects.filter(user__username=username).first()

#     @database_sync_to_async
#     def get_chat_model(self,roomname):
#         return Chat.objects.filter(roomname=roomname).first()

#     @database_sync_to_async
#     def create_message_model(self,user_model,message,chat_model,label):
#         return Message.objects.create(author=user_model,message=message,related_chat=chat_model,label=label)
    
#     async def new_message(self,data):
#         data['label']='text'
#         user_model=await self.get_user_model(data['__str__'])
#         chat_model=await self.get_chat_model(data['roomname'])
#         message_model= await self.create_message_model(user_model,data['message'],chat_model,'text')
#         result=await self.message_serializers(message_model,False)
#         result['command']='new_message'
#         await self.send_to_chat_message(result)
#         await self.notif(data)
    
#     @database_sync_to_async
#     def get_chat_members(self,roomname):
#         members = Chat.objects.get(roomname = roomname).members.all()
#         members_list=[]
#         for _ in members:
#             members_list.append(_.user.username)
        
#         return members_list
          
#     async def notif(self,data):
#         members_list=await self.get_chat_members(data['roomname'])        
#         await self.channel_layer.group_send(
#             'chat_listener',
#             {
#                 'type':'chat_message',
#                 'message':data['message'],
#                 'label':data['label'],
#                 'members_list':members_list,
#                 'roomname':data['roomname'],
#                 '__str__':data['__str__']
#             }
#         )
       
#     @database_sync_to_async
#     def fetch_message_queries(self,data):
#         return Message.all_message(self,data['roomname'])
        
#     async def fetch_messages(self,data):
#         messages=await self.fetch_message_queries(data)
#         message_json=await self.message_serializers(messages,True)
#         result={
#             'message':message_json,
#             'command':'fetch_message'
#         }
#         await self.chat_message(result)

#     async def image(self,data):
#         data['label']='image'
#         await self.notif(data)
#         chat_model=await self.get_chat_model(data['roomname'])
#         user_model = await self.get_user_model(data['__str__'])
#         message_model=await self.create_message_model(user_model,data['message'],chat_model,'image')
#         result=await self.message_serializers(message_model,False)
#         result['command']='image'
#         await self.send_to_chat_message(result)
    
    
#     commands={
#         'fetch_message':fetch_messages,
#         'new_message':new_message,
#         'image':image
#     }
    
#     async def receive(self, text_data):
#         data=json.loads(text_data)
#         command=data['command']
#         await self.commands[command](self,data) 
        
#     async def send_to_chat_message(self,data):
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type':'chat_message',
#                 'message':data['message'],
#                 'command':data['command'],
#                 '__str__':data['__str__'],
#                 'label':data['label'],
#                 'local_date':data['local_date'],
#                 'get_user_profile':data['get_user_profile']
#             })

#     async def chat_message(self,data):   
#         await self.send(text_data=json.dumps(data))





    # @database_sync_to_async
    # def get_online_users(self,roomname):
    #     # users=User.objects.filter(Q(chat__roomname=roomname)and Q(profile__status=True))
    #     # users=User.objects.filter(profile__chat__roomname=roomname)
    #     users=Chat.objects.filter(roomname = roomname)
    
       