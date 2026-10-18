from rest_framework import serializers


class VisitInputSerializer(serializers.Serializer):
    """Validates the payload the frontend sends."""

    path       = serializers.CharField(max_length=500)
    referrer   = serializers.CharField(max_length=500, required=False, allow_blank=True)
    session_id = serializers.CharField(max_length=64,  required=False, allow_blank=True)

    def validate_path(self, value):
        # Only store the path portion, no query string, no domain
        from urllib.parse import urlparse
        parsed = urlparse(value)
        path = parsed.path or '/'
        return path[:500]