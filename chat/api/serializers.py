from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from chat.models import Chat,Message

class ChatListSerializer(ModelSerializer):
    class Meta:
        model=Chat
        exclude=['members']

class ChatDetailSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields='__all__'

class MessageListSerializer(ModelSerializer):
    class Meta:
        model=Message
        fields=['id','author','get_message','related_chat','local_date']

class MessageDetailSerializer(ModelSerializer):
    class Meta:
        model=Message
        fields='__all__'



