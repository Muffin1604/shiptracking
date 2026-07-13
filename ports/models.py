from django.db import models


class PortCallCache(models.Model):
    """Cached port-calls-by-port response from Data Docked."""

    port_unlocode = models.CharField(max_length=20, db_index=True)
    search_type = models.CharField(max_length=20, blank=True, default="")
    vessel_type = models.CharField(max_length=50, blank=True, default="")
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "port call caches"
        constraints = [
            models.UniqueConstraint(
                fields=["port_unlocode", "search_type", "vessel_type"],
                name="unique_port_call_cache",
            )
        ]

    def __str__(self):
        return f"{self.port_unlocode} ({self.search_type or 'all'})"
