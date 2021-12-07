from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,EditUserForm,ChangeProfileImage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import Chat
from .models import Profile
import base64

@login_required(login_url='/login')
def edit_user_profile(request):
    user=request.user
   
    if request.method=='POST':
        form=EditUserForm(request.POST ,initial={'full_name': user.first_name,'email':user.email,'location':user.profile.location})
        image_form=ChangeProfileImage(request.POST, request.FILES)
        if form.is_valid():
            m = Profile.objects.get(pk=user.id)
            # if form.cleaned_data['image']:
            #     m.profile_image = form.cleaned_data['image']
            #     # m.save_image_field()
        
            if form.cleaned_data.get('location') :
                m.location =form.cleaned_data.get('location')
            else:
                m.location=''

            m.save()
        
           
            if form.cleaned_data.get('full_name') :
                user.first_name =form.cleaned_data.get('full_name')
            else:
                user.first_name=''

            
            
            if form.cleaned_data.get('email') :
                user.email = form.cleaned_data.get('email')

            user.save()
        
        if image_form.is_valid():
            user.profile.profile_image=image_form.cleaned_data['image']
            user.save()
            user.profile.save_image_field()
    
    else:
        form=EditUserForm(initial={'full_name': user.first_name,'email':user.email,'location':user.profile.location})
        image_form=ChangeProfileImage()

    user=request.user
    chat_rooms=Chat.objects.filter(members__user=request.user)
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
        'profile_form':form,
        'users':users,
        'users':users,
        'image_form':image_form
    }

    return render(request, 'editProfile.html',context)



def logoutUser(request):
    logout(request)
    return redirect('chat:index')

def signin_page(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
    

    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat:index')
    


    context = {
        'login_form': login_form
    }
    return render(request,'authentication/sign-in.html',context)



def save_image_field(image):
       ext = image.name.split('.')[-1]
       encoded_string=base64.b64encode(image.read())
       ch=encoded_string.decode('utf-8')
       return f'data:image/{ext};base64,{ch}'

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
    
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        user=User.objects.create_user(username=user_name, email=email, password=password)
        login(request, user)
        return redirect('chat:index')
    context={
        'signup_form':register_form
    }
    return render(request,'authentication/sign-up.html',context)