from django.urls import path
from .views import signin_page,signup_page,logoutUser,edit_user_profile

app_name='authentication'

urlpatterns = [
    path('',signin_page,name='sign-in'),
    path('edit/',edit_user_profile,name='edit'),
    path('sign-up/',signup_page,name='sign-up'),
    path('log-out',logoutUser,name='log-out'),
]