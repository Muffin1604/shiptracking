from django.db import models


class VesselInfo(models.Model):
    """Static vessel details from Data Docked get-vessel-info."""

    imo = models.CharField(max_length=20, unique=True, db_index=True)
    mmsi = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    ship_type = models.CharField(max_length=100, blank=True)
    callsign = models.CharField(max_length=20, blank=True)
    teu = models.CharField(max_length=50, blank=True)
    length = models.CharField(max_length=50, blank=True)
    beam = models.CharField(max_length=50, blank=True)
    draught = models.CharField(max_length=50, blank=True)
    eni = models.CharField(max_length=50, blank=True)
    eta_utc = models.CharField(max_length=100, blank=True)
    deadweight = models.CharField(max_length=50, blank=True)
    speed = models.CharField(max_length=50, blank=True)
    atd_utc = models.CharField(max_length=100, blank=True)
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=20, blank=True)
    heading = models.CharField(max_length=20, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    hull = models.CharField(max_length=100, blank=True)
    builder = models.CharField(max_length=255, blank=True)
    material = models.CharField(max_length=100, blank=True)
    place_of_build = models.CharField(max_length=255, blank=True)
    position_received = models.CharField(max_length=100, blank=True)
    ballast_water = models.CharField(max_length=100, blank=True)
    crude_oil = models.CharField(max_length=50, blank=True)
    fresh_water = models.CharField(max_length=50, blank=True)
    gas = models.CharField(max_length=50, blank=True)
    grain = models.CharField(max_length=50, blank=True)
    bale = models.CharField(max_length=50, blank=True)
    unlocode_destination = models.CharField(max_length=20, blank=True)
    unlocode_lastport = models.CharField(max_length=20, blank=True)
    last_port = models.CharField(max_length=255, blank=True)
    country_iso = models.CharField(max_length=10, blank=True)
    type_specific = models.CharField(max_length=100, blank=True)
    navigational_status = models.CharField(max_length=100, blank=True)
    gross_tonnage = models.CharField(max_length=50, blank=True)
    net_tonnage = models.CharField(max_length=50, blank=True)
    year_of_built = models.CharField(max_length=10, blank=True)
    engine = models.JSONField(default=dict, blank=True)
    management = models.JSONField(default=dict, blank=True)
    update_time = models.CharField(max_length=100, blank=True)
    data_source = models.CharField(max_length=50, blank=True)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "vessel info"

    def __str__(self):
        return f"{self.name} ({self.imo})"


class VesselLocation(models.Model):
    """Tracking snapshot from Data Docked get-vessel-location."""

    vessel = models.ForeignKey(
        VesselInfo, on_delete=models.CASCADE, related_name="locations"
    )
    latitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    eta_utc = models.CharField(max_length=100, blank=True)
    atd_utc = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=20, blank=True)
    heading = models.CharField(max_length=20, blank=True)
    speed = models.CharField(max_length=50, blank=True)
    draught = models.CharField(max_length=50, blank=True)
    navigational_status = models.CharField(max_length=100, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    last_port = models.CharField(max_length=255, blank=True)
    callsign = models.CharField(max_length=20, blank=True)
    position_received = models.CharField(max_length=100, blank=True)
    update_time = models.CharField(max_length=100, blank=True)
    unlocode_destination = models.CharField(max_length=20, blank=True)
    unlocode_lastport = models.CharField(max_length=20, blank=True)
    type_specific = models.CharField(max_length=100, blank=True)
    data_source = models.CharField(max_length=50, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.vessel.imo} @ {self.recorded_at}"


class VesselWeather(models.Model):
    """Weather snapshot from Data Docked get-vessel-weather."""

    vessel = models.ForeignKey(
        VesselInfo, on_delete=models.CASCADE, related_name="weather_readings"
    )
    temperature = models.CharField(max_length=50, blank=True)
    wind_speed = models.CharField(max_length=50, blank=True)
    waves = models.CharField(max_length=50, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name_plural = "vessel weather"

    def __str__(self):
        return f"{self.vessel.imo} weather @ {self.recorded_at}"
