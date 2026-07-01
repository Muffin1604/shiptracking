from django.contrib import admin

from vessels.models import VesselInfo, VesselLocation, VesselWeather


@admin.register(VesselInfo)
class VesselInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "imo", "mmsi", "ship_type", "created_at")
    search_fields = ("name", "imo", "mmsi")


@admin.register(VesselLocation)
class VesselLocationAdmin(admin.ModelAdmin):
    list_display = ("vessel", "latitude", "longitude", "speed", "created_at")
    list_filter = ("vessel",)


@admin.register(VesselWeather)
class VesselWeatherAdmin(admin.ModelAdmin):
    list_display = ("vessel", "temperature", "wind_speed", "waves", "created_at")
    list_filter = ("vessel",)
