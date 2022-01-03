from django.urls import path
from. import views

app_name='chat-api'
urlpatterns=[
    path('chat/',views.ChatListAPIView.as_view(),name='chat-list'),
    path('chat/create/',views.ChatCreateAPIView.as_view(),name='chat-create'),
    path('chat/<int:id>',views.ChatDetailAPIView.as_view(),name='chat-detail'),
    # path('chat/<int:id>/delete/',views.ChatDeleteAPIView.as_view(),name='chat-delete'),
    path('chat/<int:id>/edit/',views.ChatEditAPIView.as_view(),name='chat-edit'),
    # # path('chat/<int:id>/update/',views.ChatUpdateAPI.as_view(),name='chat-update'),
    # # path('chat/<str:roomname>/update/',views.ChatUpdateAPI.as_view(),name='chat-delete'),
    path('message/',views.MessageListAPIView.as_view(),name='message-api'),
    path('message/create/',views.MessageCreateAPIView.as_view(),name='message-create'),
    path('message/<id>',views.MessageDetailAPIView.as_view(),name='message-detail'),
    path('message/<id>/edit/',views.MessagEditAPIView.as_view(),name='message-delete'),
]