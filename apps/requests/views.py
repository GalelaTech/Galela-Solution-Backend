import hashlib
import os
import random
import string

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ServiceRequest, RequestFile
from .serializers import ServiceRequestCreateSerializer


MAX_FILES      = 5
MAX_FILE_BYTES = 10 * 1024 * 1024
EXT_TO_MIME = {
    '.pdf':  {'application/pdf'},
    '.doc':  {'application/msword'},
    '.docx': {'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
    '.xls':  {'application/vnd.ms-excel'},
    '.xlsx': {'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'},
    '.jpg':  {'image/jpeg'},
    '.jpeg': {'image/jpeg'},
    '.png':  {'image/png'},
    '.webp': {'image/webp'},
}

def generate_reference() -> str:
    date = timezone.now().strftime('%Y%m%d')
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"GS-{date}-{rand}"


def hash_ip(request) -> str:
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '')
    salt = timezone.now().strftime('%Y-%m-%d')
    return hashlib.sha256(f"{ip}{salt}{settings.SECRET_KEY[:8]}".encode()).hexdigest()


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def create_request(request):
    """
    POST /api/requests/
    Accepts multipart/form-data with fields:
      name, email, phone, company, service, budget,
      date (preferred_date), message, consent, files[]
    """
    data = request.data.copy()

    # Frontend sends 'date'; the model field is 'preferred_date'
    if 'date' in data and data['date']:
        data['preferred_date'] = data['date']
    elif 'date' in data:
        data.pop('date')

    serializer = ServiceRequestCreateSerializer(data=data)
    if not serializer.is_valid():
        return Response(
            {"detail": "Invalid submission.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    uploaded = request.FILES.getlist('files') or []
    if len(uploaded) > MAX_FILES:
        return Response(
            {"detail": f"You can attach at most {MAX_FILES} files."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for f in uploaded:
        ext = os.path.splitext(f.name)[1].lower()

        # Extension must be in our whitelist
        if ext not in EXT_TO_MIME:
            return Response(
                {"detail": f"File type not allowed: {f.name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if f.content_type not in EXT_TO_MIME[ext]:
            return Response(
                {"detail": (
                    f"Content-type mismatch for {f.name}. "
                    f"Got '{f.content_type}', expected one of {sorted(EXT_TO_MIME[ext])}."
                )},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if f.size > MAX_FILE_BYTES:
            return Response(
                {"detail": f"File too large: {f.name} (max {MAX_FILE_BYTES // (1024*1024)} MB)."},
                status=status.HTTP_400_BAD_REQUEST,
            )


    validated = serializer.validated_data
    consent_value = validated.pop('consent', False)

    reference = generate_reference()
    while ServiceRequest.objects.filter(reference=reference).exists():
        reference = generate_reference()

    service_request = ServiceRequest.objects.create(
        reference=reference,
        consent_given=bool(consent_value),
        ip_hash=hash_ip(request),
        user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:500],
        **validated,
    )

    for f in uploaded:
        RequestFile.objects.create(
            request=service_request,
            file_name=f.name[:255],
            content_type=f.content_type or 'application/octet-stream',
            size=f.size,
            data=f.read(),
        )

    return Response(
        {
            "id":         service_request.id,
            "reference":  service_request.reference,
            "status":     service_request.status,
            "created_at": service_request.created_at.isoformat(),
            "files": [
                {
                    "id":          rf.id,
                    "file_name":   rf.file_name,
                    "size":        rf.size,
                    "uploaded_at": rf.uploaded_at.isoformat(),
                }
                for rf in service_request.files.all()
            ],
        },
        status=status.HTTP_201_CREATED,
    )