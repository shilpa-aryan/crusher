from rest_framework.permissions import BasePermission

# from rest_framework import permissions

class IsAdmin(BasePermission):
    """
    Handles permissions for users. The basic rules are:
     - owner may GET, PUT, POST, DELETE
     - nobody else can access
    """
    # 1- Administrator
    # 2 - Site Manager
    def has_permission(self, request, view):
        if request.method=='GET':
            return request.user.user_type ==  1,2
        if request.method=='POST':
            return request.user.user_type ==  1
        if request.method=='PUT':
            return request.user.user_type ==  1
        if request.method=='PATCH':
            return request.user.user_type ==  1
        if request.method=='DELETE':
            return request.user.user_type ==  1
       

class IsSiteManager(BasePermission):
    """
    Handles permissions for users. The basic rules are:
     - owner may GET, PUT, POST, DELETE
     - nobody else can access
    """
    # 1- Administrator
    # 2 - Site Manager
    def has_permission(self, request, view):
        if request.method=='GET':
            return request.user.user_type ==  1,2
        if request.method=='POST':
            return request.user.user_type ==  2
        if request.method=='PUT':
            return request.user.user_type ==  2
        if request.method=='PATCH':
            return request.user.user_type ==  2
        if request.method=='DELETE':
            return request.user.user_type ==  2
       

class IsAllowedToRead(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_allowed_to_read == "YES"










