from django.contrib import admin
from .models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = [
        'created_at', 'ip', 'country', 'path',
        'as_name', 'city',
    ]
    list_filter = ['country_code', 'continent', 'visit_date']
    search_fields = ['ip', 'as_name', 'path', 'city']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    readonly_fields = [
        'ip', 'session_id', 'path', 'referrer', 'user_agent',
        'country', 'country_code', 'continent',
        'region', 'city', 'postal', 'coordinates',
        'asn', 'as_name', 'as_domain', 'as_type', 'hostname',
        'created_at', 'visit_date',
    ]

    fieldsets = (
        ('Identity', {'fields': ('ip', 'session_id')}),
        ('Page',     {'fields': ('path', 'referrer', 'user_agent')}),
        ('Geo',      {'fields': ('country', 'country_code', 'continent',
                                 'region', 'city', 'postal', 'coordinates')}),
        ('Network',  {'fields': ('asn', 'as_name', 'as_domain', 'as_type', 'hostname')}),
        ('Time',     {'fields': ('created_at', 'visit_date')}),
    )

    def has_add_permission(self, request):
        return False  # visits are only created by the API