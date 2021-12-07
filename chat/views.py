from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Chat
from user.models import Profile
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User
from django.db.models import Q
import random
import string
@login_required(login_url='authentication:sign-in')
def index(request):
    user=request.user
    chat_rooms=Chat.objects.filter(members__user=user)
    users=[user_model.username for user_model in User.objects.all()]  
    private=[]
    for chat in chat_rooms:
        if chat.label=='contact':
            contact=chat.members.all().exclude(user=user).first()
          
            private.append(contact)
        else:
            private.append(None)

    chat_rooms=zip(private,chat_rooms)
    context={
        'chat_rooms':chat_rooms,
        'user':user,
        'users':users
    }
    return render(request,'chat/index.html',context)



@login_required(login_url='authentication:sign-in')
def room(request,room_name):
    user=request.user
    users=[user_model.username for user_model in User.objects.all()]  
    chat=Chat.objects.filter(roomname=room_name)
    private=None
    
    if not chat.exists() :
        chat=Chat.objects.create(roomname=room_name,author=user.profile,label='group')
        profile_model=Profile.objects.filter(user=user).first()
        chat.members.add(profile_model)
    else:
        chat=chat.first()
        if chat.label=='group':
            profile_model=Profile.objects.filter(user=user).first()
            chat.members.add(profile_model)
        elif chat.label=='contact':
            private=chat.members.all().exclude(user=user).first()
    
    chat_rooms=Chat.objects.filter(members__user=user)
    private_chats=[]
    for _ in chat_rooms:
        if _.label=='contact':
            contact=_.members.all().exclude(user=user).first()
          
            private_chats.append(contact)
        else:
            private_chats.append(None)

    chat_rooms=zip(private_chats,chat_rooms)

    permission=True if (chat.author==request.user.profile) else False

    context={
        'chat':chat,
        "room_name":room_name,
        'username':mark_safe(json.dumps(request.user.username)),
        'chat_rooms':chat_rooms,
        'user':user,
        'users':users,
        'private':private,
        'permission':permission
    }

    return render(request,'chat/room.html',context)

@login_required(login_url='authentication:sign-in')
def delete_chat(request,room_name):
    Chat.objects.filter(roomname=room_name).delete()
    return redirect('chat:index')



@login_required(login_url='authentication:sign-in')
def left_chat(request,room_name):
    chat=Chat.objects.filter(roomname=room_name).first()
    chat.members.remove(request.user.profile)
   
    if chat.members.all().count()==0:
        Chat.objects.filter(roomname=room_name).delete()
    return redirect('chat:index')

@login_required(login_url='authentication:sign-in')
def cleare_chat(request,room_name):
    chat=Chat.objects.get(roomname=room_name)
    chat.message_set.all().delete()
    return redirect('chat:room',room_name)

@login_required(login_url='authentication:sign-in')
def contact(request,contact_name):
    room_name= f"{''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) }"
    if contact_name != request.user.username :
        user=request.user.profile
        othercontact=Profile.objects.get(user__username=contact_name)
        chat_model=Chat.objects.filter(members=user , label='contact' ).filter(members=othercontact).distinct()
        
        if not chat_model.exists():
            chat_model=Chat.objects.create(roomname=room_name,label='contact',author=request.user.profile)
            chat_model.members.add(user)
            chat_model.members.add(othercontact)
        else:
            chat_model=chat_model.first()
        
        return redirect('chat:room',room_name=chat_model.roomname)

