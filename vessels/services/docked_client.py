import os

import requests

BASE_URL = "https://datadocked.com/api/vessels_operations"


class DockedAPIError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class DockedClient:
    def __init__(self):
        api_key = os.getenv("DATA_DOCKED_API_KEY")
        if not api_key:
            raise DockedAPIError("DATA_DOCKED_API_KEY is not set")
        self.headers = {
            "accept": "application/json",
            "x-api-key": api_key,
        }

    def _request(self, endpoint, params):
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30,
        )
        if not response.ok:
            raise DockedAPIError(
                response.text or f"Docked API error ({response.status_code})",
                status_code=response.status_code,
            )
        return response.json()

    def _get(self, endpoint, imo_or_mmsi):
        return self._request(endpoint, {"imo_or_mmsi": imo_or_mmsi})

    def get_vessel_info(self, imo_or_mmsi):
        return self._get("get-vessel-info", imo_or_mmsi)

    def get_vessel_location(self, imo_or_mmsi):
        return self._get("get-vessel-location", imo_or_mmsi)

    def get_vessel_weather(self, imo_or_mmsi):
        return self._get("get-vessel-weather", imo_or_mmsi)

    def get_port_calls_by_port(
        self, port_call, offset=0, search_type=None, vessel_type=None
    ):
        params = {"port_call": port_call, "offset": offset}
        if search_type:
            params["search_type"] = search_type
        if vessel_type:
            params["vessel_type"] = vessel_type
        return self._request("port-calls-by-port", params)
