from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.requests.models import ServiceRequest
from apps.analytics.models import Visit
from .permissions import HasDashboardKey
from .serializers import (
    VisitDashboardSerializer,
    RequestDashboardSerializer,
)
import base64
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from apps.requests.models import RequestFile


class DashboardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class VisitsListView(generics.ListAPIView):
    serializer_class = VisitDashboardSerializer
    permission_classes = [HasDashboardKey]
    pagination_class = DashboardPagination

    def get_queryset(self):
        queryset = Visit.objects.all().order_by('-created_at')
        
        # If the request includes ?site=injabulo, filter the queryset
        site_filter = self.request.query_params.get('site', None)
        if site_filter:
            queryset = queryset.filter(site=site_filter)
            
        return queryset


class RequestsListView(generics.ListAPIView):
    """
    GET /api/dashboard/requests/?key=SECRET&page=1
    """
    queryset           = ServiceRequest.objects.prefetch_related('files').order_by('-created_at')
    serializer_class   = RequestDashboardSerializer
    permission_classes = [HasDashboardKey]
    pagination_class   = DashboardPagination

class VisitDeleteView(APIView):
    """
    DELETE /api/dashboard/visits/<id>/?key=SECRET
    """
    permission_classes = [HasDashboardKey]

    def delete(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        visit.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


class RequestDeleteView(APIView):
    """
    DELETE /api/dashboard/requests/<id>/?key=SECRET
    Note: Deleting a request automatically deletes its files (CASCADE).
    """
    permission_classes = [HasDashboardKey]

    def delete(self, request, pk):
        try:
            service_request = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        service_request.delete()
        return Response({"detail": "Deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([HasDashboardKey])
def download_file(request, pk):
    """
    GET /api/dashboard/files/<pk>/?key=SECRET
    Streams the file back from the database.
    """
    try:
        db_file = RequestFile.objects.get(pk=pk)
    except RequestFile.DoesNotExist:
        return Response({"detail": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    # Read the binary data from the database
    file_bytes = bytes(db_file.data)
    
    # Create the response
    response = HttpResponse(file_bytes, content_type=db_file.content_type)
    
    # This header forces the browser to download the file
    response['Content-Disposition'] = f'attachment; filename="{db_file.file_name}"'
    response['Content-Length'] = str(db_file.size)
    
    return response