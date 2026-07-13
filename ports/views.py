from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ports.exceptions import DockedServiceError
from ports.serializers import PortCallCacheSerializer
from ports.services import get_port_calls_by_port
from vessels.services import DockedAPIError

VALID_SEARCH_TYPES = {"", "expected", "arrival", "departures", "in_port"}


def _handle_docked_error(exc):
    raise DockedServiceError(detail=str(exc), status_code=exc.status_code or 502)


class PortCallsByPortView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, port_unlocode):
        search_type = request.query_params.get("search_type", "")
        vessel_type = request.query_params.get("vessel_type", "")
        force = request.query_params.get("force", "").lower() in ("1", "true", "yes")

        if search_type not in VALID_SEARCH_TYPES:
            return Response(
                {
                    "detail": (
                        "search_type must be one of: expected, arrival, "
                        "departures, in_port"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cache_row, from_cache = get_port_calls_by_port(
                port_unlocode,
                search_type=search_type,
                vessel_type=vessel_type,
                force=force,
            )
        except DockedAPIError as exc:
            _handle_docked_error(exc)

        payload = PortCallCacheSerializer(cache_row).data
        payload["fromCache"] = from_cache
        return Response(payload)

    def post(self, request, port_unlocode):
        search_type = request.data.get("search_type", "")
        vessel_type = request.data.get("vessel_type", "")

        if search_type not in VALID_SEARCH_TYPES:
            return Response(
                {
                    "detail": (
                        "search_type must be one of: expected, arrival, "
                        "departures, in_port"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cache_row, from_cache = get_port_calls_by_port(
                port_unlocode,
                search_type=search_type,
                vessel_type=vessel_type,
                force=True,
            )
        except DockedAPIError as exc:
            _handle_docked_error(exc)

        payload = PortCallCacheSerializer(cache_row).data
        payload["fromCache"] = from_cache
        return Response(payload, status=status.HTTP_200_OK)
