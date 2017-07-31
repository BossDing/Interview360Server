from rest_framework import permissions
from .models import CompanyMember

class AllowedToUpdateCompany(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in ['PUT', 'DELETE']: return False

        try:
            owner_role = CompanyMember.objects.get(user_id=request.user.id,
                                                   company_id=obj.id,
                                                   role='owner')
        except CompanyMember.DoesNotExist:
            owner_role = None

        if owner_role != None:
            return True
