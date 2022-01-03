from rest_framework import generics
from chat.models import Chat,Message
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .permissions import OwnerCanManageOrReadOnly,MemberCanSee,MemberCanSeeMessage,OwnerCanManageMessage
from rest_framework.permissions import (
    AllowAny, 
    IsAdminUser,
    IsAuthenticated
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .serializers import (ChatListSerializer,
                          ChatDetailSerializer,
                          MessageListSerializer,
                          MessageDetailSerializer)


class ChatListAPIView(generics.ListAPIView):
    serializer_class = ChatListSerializer
    filter_backends=[SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields=['author','label','roomname','members',]
    filterset_fields=['author','roomname','label']
    search_fields = ['roomname','label','members__user__username']
    permission_classes = [OwnerCanManageOrReadOnly,]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset=Chat.objects.all()
        elif not self.request.user.is_anonymous:
            queryset=Chat.objects.filter(members=self.request.user.profile)
        else:
            raise PermissionDenied

        query=self.request.GET.get('q')
        if query:
            queryset=Chat.objects.filter(
                Q(roomname__icontains=query)|
                Q(members__user__username__icontains=query)|
                Q(label__icontains=query)
            )
        return queryset

class ChatDetailAPIView(generics.RetrieveAPIView):
    queryset=Chat.objects.all()
    serializer_class=ChatDetailSerializer
    lookup_field='id'
    permission_classes=[MemberCanSee]
    
class ChatEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ChatDetailSerializer
    lookup_field='id'
    permission_classes=  [OwnerCanManageOrReadOnly,]
    queryset=Chat.objects.all()
    # def perform_destroy(self, instance):
    #     if instance.author!=self.request.user.profile:
    #         raise PermissionDenied

    # def perform_update(self, serializer):
    #     return super().perform_update(serializer)

class ChatCreateAPIView(generics.CreateAPIView):
    serializer_class=ChatDetailSerializer
    permission_classes=  [IsAuthenticated]
    queryset=Chat.objects.all()



# --------------------------Message---------------------------
class MessageListAPIView(generics.ListAPIView):
    serializer_class=MessageListSerializer
    permission_classes=  [MemberCanSeeMessage,]
    filter_backends=[SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields='__all__'
    filterset_fields=['author','related_chat','label']
    search_fields = ['author__user__username','related_chat__roomname','related_chat__members__user__username','label','message']
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset=Message.objects.all()
        elif not self.request.user.is_anonymous:
            queryset=Message.objects.filter(related_chat__members=self.request.user.profile)
        else:
            raise PermissionDenied
        return queryset

class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class=MessageDetailSerializer
    queryset=Message.objects.all()
    permission_classes=  [IsAuthenticated]

class MessageDetailAPIView(generics.RetrieveAPIView):
    lookup_field='id'
    serializer_class=  MessageDetailSerializer
    queryset=Message.objects.all()
    permission_classes=  [MemberCanSeeMessage,]

class MessagEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=MessageDetailSerializer
    lookup_field='id'
    permission_classes=  [OwnerCanManageMessage,]
    queryset=Message.objects.all()
    

