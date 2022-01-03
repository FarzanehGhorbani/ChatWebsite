from django.urls import path
from . import views

app_name='user-api'
urlpatterns=[
    path('users/',views.UserListAPIView.as_view(),name='users-list'),
    path('users/create',views.UserCreateAPIView.as_view(),name='users-create'),
    path('users/<int:id>/edit',views.UserEditAPIVIew.as_view(),name='users-create')
]