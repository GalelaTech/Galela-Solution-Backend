from django.conf import settings
from rest_framework import permissions


class HasDashboardKey(permissions.BasePermission):
    """
    Allows access only if ?key= matches settings.DASHBOARD_KEY.
    """

    def has_permission(self, request, view):
        expected = getattr(settings, 'DASHBOARD_KEY', '').strip()
        if not expected:
            return False
        provided = request.query_params.get('key', '').strip()
        return provided == expected