from django.urls import path
from .views import index,room,contact,delete_chat,cleare_chat,left_chat

app_name='chat'
urlpatterns = [
    path('',index,name='index'),
    path('delete/<str:room_name>/',delete_chat,name='delete'),
    path('cleare/<str:room_name>/',cleare_chat,name='cleare'),
    path('left/<str:room_name>/',left_chat,name='left'),
    path('<str:room_name>/',room,name='room'),
    path('contact/<str:contact_name>/',contact,name='contact'),
    
]