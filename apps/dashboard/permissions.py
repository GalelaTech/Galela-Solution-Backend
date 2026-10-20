from rest_framework import permissions
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired

class HasDashboardKey(permissions.BasePermission):
    """
    Checks for a valid Bearer token in the Authorization header.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return False
            
        token = auth_header.split(' ')[1]
        
        try:
            # Token is valid for 7 days (604800 seconds)
            signing.loads(token, salt="dashboard-auth", max_age=604800)
            return True
        except (BadSignature, SignatureExpired):
            return False