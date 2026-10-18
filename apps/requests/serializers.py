from rest_framework import serializers
from .models import ServiceRequest, RequestFile


class RequestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestFile
        fields = ['id', 'file_name', 'content_type', 'size', 'uploaded_at']
        read_only_fields = fields


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    consent = serializers.CharField(write_only=True, required=True)
    files   = RequestFileSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            'name', 'email', 'phone', 'company',
            'service', 'budget', 'preferred_date', 'message',
            'consent', 'files',
        ]
        extra_kwargs = {
            'budget':         {'required': False, 'allow_blank': True},
            'company':        {'required': False, 'allow_blank': True},
            'preferred_date': {'required': False, 'allow_null':   True},
        }

    def validate_consent(self, value):
        if str(value).lower() not in ('true', '1', 'yes', 'on'):
            raise serializers.ValidationError(
                "You must agree to be contacted to submit this request."
            )
        return True

    def validate_service(self, value):
        valid = [c[0] for c in ServiceRequest.SERVICE_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(
                f"Service must be one of: {', '.join(valid)}"
            )
        return value

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Please describe what you need in at least 10 characters."
            )
        return value.strip()