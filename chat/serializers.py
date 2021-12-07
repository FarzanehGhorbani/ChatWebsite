from rest_framework import serializers
from .models import Message
from user.models import Profile

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__','message','local_date','label','get_user_profile']


class OnlineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['__str__','image_field','get_contact_url']