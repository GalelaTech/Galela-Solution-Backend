from django.db import models


class Visit(models.Model):
    """
    One row per page view. Raw IP stored (no hashing).
    Geo data is filled by ipinfo.io on the free tier.
    Region, city, postal, coordinates, as_type, hostname stay blank
    unless we later upgrade to a paid plan or add reverse DNS.
    """

    # ── Identity ────────────────────────────────────────────
    site       = models.CharField(max_length=50, default='galela', db_index=True)
    ip         = models.GenericIPAddressField(db_index=True)
    session_id = models.CharField(max_length=64, blank=True, db_index=True)

    # ── Page info ───────────────────────────────────────────
    path       = models.CharField(max_length=500)
    referrer   = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # ── Geo (from ipinfo free) ──────────────────────────────
    country      = models.CharField(max_length=100, blank=True)   # "South Africa"
    country_code = models.CharField(max_length=2,   blank=True)   # "ZA"
    continent    = models.CharField(max_length=50,  blank=True)   # "Africa"

    # ── Geo (needs paid plan — left blank for now) ──────────
    region       = models.CharField(max_length=100, blank=True)
    city         = models.CharField(max_length=100, blank=True)
    postal       = models.CharField(max_length=20,  blank=True)
    coordinates  = models.CharField(max_length=50,  blank=True)

    # ── Network / ASN (from ipinfo free) ────────────────────
    asn       = models.CharField(max_length=20,  blank=True)   # "AS37105"
    as_name   = models.CharField(max_length=255, blank=True)   # "Rain Group Holdings (Pty) Ltd"
    as_domain = models.CharField(max_length=100, blank=True)   # "rain.co.za"
    as_type   = models.CharField(max_length=50,  blank=True)   # blank for now
    hostname  = models.CharField(max_length=255, blank=True)   # blank for now

    # ── Timestamps ──────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    visit_date = models.DateField(db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ip', 'visit_date']),
            models.Index(fields=['visit_date', 'path']),
            models.Index(fields=['country_code', 'visit_date']),
        ]
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'

    def __str__(self):
        where = self.country or 'Unknown'
        return f"{where} — {self.path} @ {self.created_at:%Y-%m-%d %H:%M}"