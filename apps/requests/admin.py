from django.contrib import admin
from .models import ServiceRequest, RequestFile


class RequestFileInline(admin.TabularInline):
    model = RequestFile
    extra = 0
    readonly_fields = ['file_name', 'content_type', 'size', 'uploaded_at']
    can_delete = True


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display    = ['reference', 'name', 'service', 'status', 'created_at']
    list_filter     = ['status', 'service', 'created_at']
    search_fields   = ['reference', 'name', 'email', 'phone', 'message']
    readonly_fields = ['reference', 'ip_hash', 'user_agent', 'created_at', 'updated_at']
    inlines         = [RequestFileInline]
    date_hierarchy  = 'created_at'
    ordering        = ['-created_at']

    fieldsets = (
        ('Reference', {'fields': ('reference', 'status', 'created_at', 'updated_at')}),
        ('Contact',   {'fields': ('name', 'email', 'phone', 'company')}),
        ('Request',   {'fields': ('service', 'budget', 'preferred_date', 'message', 'consent_given')}),
        ('Metadata',  {'classes': ('collapse',), 'fields': ('ip_hash', 'user_agent')}),
    )


@admin.register(RequestFile)
class RequestFileAdmin(admin.ModelAdmin):
    list_display    = ['file_name', 'request', 'size', 'uploaded_at']
    search_fields   = ['file_name', 'request__reference']
    readonly_fields = ['request', 'file_name', 'content_type', 'size', 'data', 'uploaded_at']