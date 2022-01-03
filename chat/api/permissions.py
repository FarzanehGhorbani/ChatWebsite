from rest_framework.permissions import BasePermission,SAFE_METHODS


class OwnerCanManageOrReadOnly(BasePermission):
    message=''

    def has_permission(self, request, view):
        self.message = 'Your request does no any permissions or your are not'
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_anonymous:
            return True
        else :
            return False

        
    def has_object_permission(self,request, view,obj):
        self.message='You must be the owner'
        if request.user.is_superuser:
            return True
        return request.user==obj.author

class MemberCanSee(BasePermission):
    message=''

    def has_permission(self, request, view):
        self.message = 'You are anonymuse'
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_anonymous:
            return True
        else :
            return False
    def has_object_permission(self,request, view,obj):
        self.message='you must be member of chat'
        if request.user.is_superuser:
            return True
        elif request.user.profile in obj.members.all():
            return True
        else:
            return False


class MemberCanSeeMessage(BasePermission):
    message=''
    
    def has_permission(self, request, view):
        self.message = 'You are anonymuse'
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_anonymous:
            return True
            
        else :
            return False
    
    def has_object_permission(self,request, view,obj):
        self.message='you must be member of chat'
        if request.user.is_superuser:
            return True
        elif request.user.profile in obj.related_chat.members.all():
            return True
        else:
            return False


class OwnerCanManageMessage(BasePermission):
    message=''

    def has_permission(self, request, view):
        self.message = 'You are anonymuse'
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_anonymous:
            return True
        else :
            return False
    
    def has_object_permission(self,request, view,obj):
        self.message='you must be member of chat'
  
        if request.user.is_superuser:
            return True
        return request.user==obj.author