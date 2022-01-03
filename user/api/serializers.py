from rest_framework.serializers import ModelSerializer
from user.models import Profile

class UserListSerializer(ModelSerializer):
    class Meta:
        model=Profile
        exclude =['image_field',]

class UserDetialSerializer(ModelSerializer):
    class Meta:
        model=Profile
        exclude=['image_field',]