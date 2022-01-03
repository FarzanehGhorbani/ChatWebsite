from django.db.models import query
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from user.models import Profile
from .serializers import UserListSerializer,UserDetialSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from chat.models import Chat
from django.core.exceptions import PermissionDenied

class UserListAPIView(generics.ListAPIView):
    serializer_class=UserListSerializer
    filter_backends=[SearchFilter,OrderingFilter]
    search_fields=['user__username']
    ordering_fields=['user__username','id','timestamp']
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset=Profile.objects.all()
        elif not self.request.user.is_anonymous:
            query=Chat.objects.filter(members=self.request.user.profile,label='contact')
            l=set()
            for chat in query:
                for member in chat.members.all():
                    l.add(member)
            l.add(self.request.user.profile)
            queryset=list(l)
        else:
            raise PermissionDenied

        return queryset

class UserCreateAPIView(generics.CreateAPIView):
    queryset=Profile.objects.all()
    serializer_class=UserDetialSerializer
    permission_classes=[IsAdminUser]
    lookup_field='id'

    # def perform_create(self,serializer):
    #     serializer.save(image_field=)


class UserEditAPIVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset=Profile.objects.all()
    serializer_class=UserDetialSerializer
    permission_classes=[IsAdminUser]
    lookup_field='id'



