from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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


def _resolve_vessel(imo_or_mmsi):
    vessel = VesselInfo.objects.filter(imo=imo_or_mmsi).first()
    if vessel:
        return vessel
    return VesselInfo.objects.filter(mmsi=imo_or_mmsi).first()


def _handle_docked_error(exc):
    raise DockedServiceError(detail=str(exc), status_code=exc.status_code or 502)


class VesselListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vessels = VesselInfo.objects.all().order_by("name")
        serializer = VesselInfoSerializer(vessels, many=True)
        return Response({"vessels": serializer.data})


class VesselInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, imo_or_mmsi):
        vessel = _resolve_vessel(imo_or_mmsi)
        if not vessel:
            return Response(
                {"detail": "Vessel not found. Sync info first."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(VesselInfoSerializer(vessel).data)

    def post(self, request, imo_or_mmsi):
        try:
            vessel, created, _ = sync_vessel_info(imo_or_mmsi)
        except DockedAPIError as exc:
            _handle_docked_error(exc)
        return Response(
            {"created": created, "vessel": VesselInfoSerializer(vessel).data},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class VesselTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, imo_or_mmsi):
        vessel = _resolve_vessel(imo_or_mmsi)
        if not vessel:
            return Response(
                {"detail": "Vessel not found. Sync info or track first."},
                status=status.HTTP_404_NOT_FOUND,
            )

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

    def post(self, request, imo_or_mmsi):
        try:
            location, _ = sync_vessel_location(imo_or_mmsi)
        except DockedAPIError as exc:
            _handle_docked_error(exc)
        return Response(
            {"location": VesselLocationSerializer(location).data},
            status=status.HTTP_201_CREATED,
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
