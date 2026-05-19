from vessels.models import VesselInfo, VesselLocation, VesselWeather
from vessels.services.docked_client import DockedClient


def _str(value):
    if value is None or value == "None":
        return ""
    return str(value)


def _info_fields(data):
    return {
        "imo": _str(data.get("imo")),
        "mmsi": _str(data.get("mmsi")),
        "name": _str(data.get("name")),
        "country": _str(data.get("country")),
        "ship_type": _str(data.get("shipType")),
        "callsign": _str(data.get("callsign")),
        "teu": _str(data.get("teu")),
        "length": _str(data.get("length")),
        "beam": _str(data.get("beam")),
        "draught": _str(data.get("draught")),
        "eni": _str(data.get("eni")),
        "eta_utc": _str(data.get("etaUtc")),
        "deadweight": _str(data.get("deadweight")),
        "speed": _str(data.get("speed")),
        "atd_utc": _str(data.get("atdUtc")),
        "latitude": _str(data.get("latitude")),
        "longitude": _str(data.get("longitude")),
        "course": _str(data.get("course")),
        "heading": _str(data.get("heading")),
        "destination": _str(data.get("destination")),
        "hull": _str(data.get("hull")),
        "builder": _str(data.get("builder")),
        "material": _str(data.get("material")),
        "place_of_build": _str(data.get("placeOfBuild")),
        "position_received": _str(data.get("positionReceived")),
        "ballast_water": _str(data.get("ballastWater")),
        "crude_oil": _str(data.get("crudeOil")),
        "fresh_water": _str(data.get("freshWater")),
        "gas": _str(data.get("gas")),
        "grain": _str(data.get("grain")),
        "bale": _str(data.get("bale")),
        "unlocode_destination": _str(data.get("unlocodeDestination")),
        "unlocode_lastport": _str(data.get("unlocodeLastport")),
        "last_port": _str(data.get("lastPort")),
        "country_iso": _str(data.get("countryIso")),
        "type_specific": _str(data.get("typeSpecific")),
        "navigational_status": _str(data.get("navigationalStatus")),
        "gross_tonnage": _str(data.get("grossTonnage")),
        "net_tonnage": _str(data.get("netTonnage")),
        "year_of_built": _str(data.get("yearOfBuilt")),
        "engine": data.get("engine") or {},
        "management": data.get("management") or {},
        "update_time": _str(data.get("updateTime")),
        "data_source": _str(data.get("dataSource")),
    }


def _location_fields(data):
    return {
        "latitude": _str(data.get("latitude")),
        "longitude": _str(data.get("longitude")),
        "eta_utc": _str(data.get("etaUtc")),
        "atd_utc": _str(data.get("atdUtc")),
        "course": _str(data.get("course")),
        "heading": _str(data.get("heading")),
        "speed": _str(data.get("speed")),
        "draught": _str(data.get("draught")),
        "navigational_status": _str(data.get("navigationalStatus")),
        "destination": _str(data.get("destination")),
        "last_port": _str(data.get("lastPort")),
        "callsign": _str(data.get("callsign")),
        "position_received": _str(data.get("positionReceived")),
        "update_time": _str(data.get("updateTime")),
        "unlocode_destination": _str(data.get("unlocodeDestination")),
        "unlocode_lastport": _str(data.get("unlocodeLastport")),
        "type_specific": _str(data.get("typeSpecific")),
        "data_source": _str(data.get("dataSource")),
    }


def _weather_fields(data):
    return {
        "temperature": _str(data.get("temperature")),
        "wind_speed": _str(data.get("windSpeed")),
        "waves": _str(data.get("waves")),
    }


def _get_or_create_vessel(data):
    imo = _str(data.get("imo"))
    if not imo:
        raise ValueError("API response missing imo")
    vessel, _ = VesselInfo.objects.update_or_create(
        imo=imo,
        defaults={
            "mmsi": _str(data.get("mmsi")),
            "name": _str(data.get("name")),
        },
    )
    return vessel


def sync_vessel_info(imo_or_mmsi, client=None):
    client = client or DockedClient()
    data = client.get_vessel_info(imo_or_mmsi)
    fields = _info_fields(data)
    imo = fields.pop("imo")
    vessel, created = VesselInfo.objects.update_or_create(imo=imo, defaults=fields)
    return vessel, created, data


def sync_vessel_location(imo_or_mmsi, client=None):
    client = client or DockedClient()
    data = client.get_vessel_location(imo_or_mmsi)
    vessel = _get_or_create_vessel(data)
    location = VesselLocation.objects.create(vessel=vessel, **_location_fields(data))
    return location, data


def sync_vessel_weather(imo_or_mmsi, client=None):
    client = client or DockedClient()
    data = client.get_vessel_weather(imo_or_mmsi)
    vessel = _get_or_create_vessel(data)
    weather = VesselWeather.objects.create(vessel=vessel, **_weather_fields(data))
    return weather, data
