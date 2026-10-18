from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Visit
from .serializers import VisitInputSerializer
from .services.geo import lookup_ip


def get_client_ip(request) -> str:
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '') or ''


@api_view(['POST'])
@permission_classes([AllowAny])
def track_visit(request):
    """
    POST /api/analytics/visit/
    Body: { path, referrer, session_id }
    Returns 204 No Content.
    """
    serializer = VisitInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    ip = get_client_ip(request)

    # SAST-aware date so "today" means your today
    now_sast = timezone.localtime(timezone.now())

    # Look up geo (never raises — returns blanks on failure)
    geo = lookup_ip(ip)

    site_name = request.data.get('site', 'galela')[:50]

    Visit.objects.create(
        site       = site_name,
        ip         = ip or '0.0.0.0',
        session_id = data.get('session_id', '')[:64],
        path       = data['path'],
        referrer   = data.get('referrer', '')[:500],
        user_agent = (request.META.get('HTTP_USER_AGENT') or '')[:500],

        country      = geo['country'][:100],
        country_code = geo['country_code'][:2],
        continent    = geo['continent'][:50],
        region       = geo['region'][:100],
        city         = geo['city'][:100],
        postal       = geo['postal'][:20],
        coordinates  = geo['coordinates'][:50],

        asn       = geo['asn'][:20],
        as_name   = geo['as_name'][:255],
        as_domain = geo['as_domain'][:100],
        as_type   = geo['as_type'][:50],
        hostname  = geo['hostname'][:255],

        created_at = timezone.now(),
        visit_date = now_sast.date(),
    )

    return Response(status=status.HTTP_204_NO_CONTENT)