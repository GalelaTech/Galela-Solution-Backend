from django.db import models


class ServiceRequest(models.Model):
    """
    A service request submitted from the public form.
    No user account required — this is a guest submission.
    """

    SERVICE_CHOICES = [
        ('research',    'Research & Lab Support'),
        ('technology',  'Technology & Digital'),
        ('transport',   'Transportation'),
        ('maintenance', 'Maintenance'),
        ('other',       'Other'),
    ]

    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
        ('cancelled',   'Cancelled'),
    ]

    reference = models.CharField(max_length=20, unique=True, db_index=True)

    name    = models.CharField(max_length=150)
    email   = models.EmailField()
    phone   = models.CharField(max_length=30)
    company = models.CharField(max_length=150, blank=True)

    service        = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    budget         = models.CharField(max_length=50,  blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    message        = models.TextField()

    consent_given = models.BooleanField(default=False)

    ip_hash    = models.CharField(max_length=64, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"{self.reference} — {self.name} ({self.service})"


class RequestFile(models.Model):
    """
    A file attached to a request. Stored as bytes in the DB for now.
    Will be migrated to object storage (R2) later.
    """
    request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name='files'
    )
    file_name    = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size         = models.IntegerField()
    data         = models.BinaryField()
    uploaded_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'Request File'
        verbose_name_plural = 'Request Files'

    def __str__(self):
        return f"{self.file_name} ({self.size} bytes) → {self.request.reference}"