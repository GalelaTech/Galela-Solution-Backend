from django.db import models


class ServiceCategory(models.Model):
    """
    Top-level grouping for services.
    Example: 'Research Support', 'Web Development', 'Transportation'.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="CSS icon class or identifier for the frontend",
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first",
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class ServiceOption(models.Model):
    """
    A specific service within a category.
    Example (under 'Research Support'): 'Sample preparation', 'FTIR analysis'.
    """
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='options',
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'display_order', 'name']
        unique_together = [('category', 'name')]
        verbose_name = 'Service Option'
        verbose_name_plural = 'Service Options'

    def __str__(self):
        return f"{self.category.name} — {self.name}"