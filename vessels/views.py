import json
from datetime import timedelta
from pathlib import Path

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vessels.exceptions import DockedServiceError
from vessels.models import VesselInfo
from vessels.serializers import (
    VesselInfoSerializer,
    VesselLocationSerializer,
    VesselWeatherSerializer,
)
from vessels.services import (
    DockedAPIError,
    sync_vessel_info,
    sync_vessel_location,
    sync_vessel_weather,
)

LOCATION_CACHE_MAX_AGE = timedelta(hours=24)
TEST_JSON_PATH = Path(__file__).resolve().parent / "test.json"


def _resolve_vessel(imo_or_mmsi):
    vessel = VesselInfo.objects.filter(imo=imo_or_mmsi).first()
    if vessel:
        return vessel
    return VesselInfo.objects.filter(mmsi=imo_or_mmsi).first()


def _handle_docked_error(exc):
    raise DockedServiceError(detail=str(exc), status_code=exc.status_code or 502)


class VesselListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        with TEST_JSON_PATH.open() as f:
            data = json.load(f)
        return Response(data)


class VesselInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, imo_or_mmsi):
        vessel = _resolve_vessel(imo_or_mmsi)
        if not vessel:
            try:
                vessel, _, _ = sync_vessel_info(imo_or_mmsi)
            except DockedAPIError as exc:
                _handle_docked_error(exc)
        return Response(VesselInfoSerializer(vessel).data)


class VesselTrackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, imo_or_mmsi):
        vessel = _resolve_vessel(imo_or_mmsi)
        latest = vessel.locations.first() if vessel else None
        needs_refresh = (
            vessel is None
            or latest is None
            or latest.created_at < timezone.now() - LOCATION_CACHE_MAX_AGE
        )
        if needs_refresh:
            try:
                location, _ = sync_vessel_location(imo_or_mmsi)
            except DockedAPIError as exc:
                _handle_docked_error(exc)
            vessel = location.vessel

        limit = request.query_params.get("limit")
        qs = vessel.locations.all()
        if limit:
            try:
                qs = qs[: int(limit)]
            except ValueError:
                return Response(
                    {"detail": "limit must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        locations = VesselLocationSerializer(qs, many=True).data
        return Response(
            {"latest": locations[0] if locations else None, "history": locations}
        )


class VesselWeatherView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, imo_or_mmsi):
        vessel = _resolve_vessel(imo_or_mmsi)
        if not vessel:
            return Response(
                {"detail": "Vessel not found. Sync weather first."},
                status=status.HTTP_404_NOT_FOUND,
            )

        reading = vessel.weather_readings.first()
        if not reading:
            return Response(
                {"detail": "No weather data stored."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(VesselWeatherSerializer(reading).data)

    def post(self, request, imo_or_mmsi):
        try:
            weather, _ = sync_vessel_weather(imo_or_mmsi)
        except DockedAPIError as exc:
            _handle_docked_error(exc)
        return Response(
            {"weather": VesselWeatherSerializer(weather).data},
            status=status.HTTP_201_CREATED,
        )


class VesselSyncAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, imo_or_mmsi):
        try:
            vessel, info_created, _ = sync_vessel_info(imo_or_mmsi)
            location, _ = sync_vessel_location(imo_or_mmsi)
            weather, _ = sync_vessel_weather(imo_or_mmsi)
        except DockedAPIError as exc:
            _handle_docked_error(exc)

        return Response(
            {
                "infoCreated": info_created,
                "vessel": VesselInfoSerializer(vessel).data,
                "location": VesselLocationSerializer(location).data,
                "weather": VesselWeatherSerializer(weather).data,
            },
            status=status.HTTP_201_CREATED,
        )
