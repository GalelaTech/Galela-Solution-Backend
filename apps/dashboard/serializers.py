from rest_framework import serializers

from apps.requests.models import ServiceRequest, RequestFile
from apps.analytics.models import Visit


class VisitDashboardSerializer(serializers.ModelSerializer):
    """
    Returns only fields that have a non-empty value.
    Keeps the frontend clean without extra filtering logic.
    """

    class Meta:
        model = Visit
        fields = [
            'id',
            'ip',
            'session_id',
            'path',
            'referrer',
            'user_agent',
            'country',
            'country_code',
            'continent',
            'region',
            'city',
            'postal',
            'coordinates',
            'asn',
            'as_name',
            'as_domain',
            'as_type',
            'hostname',
            'created_at',
            'visit_date',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Drop empty strings and None
        return {k: v for k, v in data.items() if v not in ('', None)}


class RequestFileDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestFile
        fields = ['id', 'file_name', 'content_type', 'size', 'uploaded_at']


class RequestDashboardSerializer(serializers.ModelSerializer):
    files = RequestFileDashboardSerializer(many=True, read_only=True)

     preferred_date = serializers.DateField(format="%Y-%m-%d", allow_null=True, required=False)

    class Meta:
        model = ServiceRequest
        fields = [
            'site', 
            'id',
            'reference',
            'name',
            'email',
            'phone',
            'company',
            'service',
            'budget',
            'preferred_date',
            'message',
            'consent_given',
            'user_agent',
            'status',
            'created_at',
            'updated_at',
            'files',
        ]