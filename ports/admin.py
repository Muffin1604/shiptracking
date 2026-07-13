from django.contrib import admin

from ports.models import PortCallCache


@admin.register(PortCallCache)
class PortCallCacheAdmin(admin.ModelAdmin):
    list_display = ("port_unlocode", "search_type", "vessel_type", "updated_at")
    list_filter = ("search_type", "vessel_type")
    search_fields = ("port_unlocode",)
