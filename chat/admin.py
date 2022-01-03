
from django.contrib import admin
from .models import Chat,Message
# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display=['__str__','author','label']



class MessageAdmin(admin.ModelAdmin):

    list_display=['get_message','__str__','get_queryset','local_date']

    # def get_queryset(self, request):
    #     qs = super(MessageAdmin, self).get_queryset(request)
    #     return self.get_ordering(request)

    def get_related_chat(self,obj):
        # if obj.related_chat.label=='contact':
        #     # return obj.related_chat.members.all().exclude(user=self.request.user).first()
        #     return self.request
        # else:
        #     return obj.related_chat
        return 

    get_related_chat.short_description='chat name'

    
admin.site.register(Chat,ChatAdmin)
admin.site.register(Message,MessageAdmin)
