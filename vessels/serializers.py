from rest_framework import serializers

from vessels.models import VesselInfo, VesselLocation, VesselWeather


class VesselInfoSerializer(serializers.ModelSerializer):
    shipType = serializers.CharField(source="ship_type", read_only=True)
    etaUtc = serializers.CharField(source="eta_utc", read_only=True)
    atdUtc = serializers.CharField(source="atd_utc", read_only=True)
    placeOfBuild = serializers.CharField(source="place_of_build", read_only=True)
    positionReceived = serializers.CharField(source="position_received", read_only=True)
    ballastWater = serializers.CharField(source="ballast_water", read_only=True)
    crudeOil = serializers.CharField(source="crude_oil", read_only=True)
    freshWater = serializers.CharField(source="fresh_water", read_only=True)
    unlocodeDestination = serializers.CharField(source="unlocode_destination", read_only=True)
    unlocodeLastport = serializers.CharField(source="unlocode_lastport", read_only=True)
    lastPort = serializers.CharField(source="last_port", read_only=True)
    countryIso = serializers.CharField(source="country_iso", read_only=True)
    typeSpecific = serializers.CharField(source="type_specific", read_only=True)
    navigationalStatus = serializers.CharField(source="navigational_status", read_only=True)
    grossTonnage = serializers.CharField(source="gross_tonnage", read_only=True)
    netTonnage = serializers.CharField(source="net_tonnage", read_only=True)
    yearOfBuilt = serializers.CharField(source="year_of_built", read_only=True)
    updateTime = serializers.CharField(source="update_time", read_only=True)
    dataSource = serializers.CharField(source="data_source", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = VesselInfo
        fields = (
            "imo",
            "mmsi",
            "name",
            "country",
            "shipType",
            "callsign",
            "teu",
            "length",
            "beam",
            "draught",
            "eni",
            "etaUtc",
            "deadweight",
            "speed",
            "atdUtc",
            "latitude",
            "longitude",
            "course",
            "heading",
            "destination",
            "hull",
            "builder",
            "material",
            "placeOfBuild",
            "positionReceived",
            "ballastWater",
            "crudeOil",
            "freshWater",
            "gas",
            "grain",
            "bale",
            "unlocodeDestination",
            "unlocodeLastport",
            "lastPort",
            "countryIso",
            "typeSpecific",
            "navigationalStatus",
            "grossTonnage",
            "netTonnage",
            "yearOfBuilt",
            "engine",
            "management",
            "updateTime",
            "dataSource",
            "createdAt",
            "updatedAt",
        )


class VesselLocationSerializer(serializers.ModelSerializer):
    imo = serializers.CharField(source="vessel.imo", read_only=True)
    mmsi = serializers.CharField(source="vessel.mmsi", read_only=True)
    name = serializers.CharField(source="vessel.name", read_only=True)
    etaUtc = serializers.CharField(source="eta_utc", read_only=True)
    atdUtc = serializers.CharField(source="atd_utc", read_only=True)
    navigationalStatus = serializers.CharField(source="navigational_status", read_only=True)
    lastPort = serializers.CharField(source="last_port", read_only=True)
    positionReceived = serializers.CharField(source="position_received", read_only=True)
    updateTime = serializers.CharField(source="update_time", read_only=True)
    unlocodeDestination = serializers.CharField(source="unlocode_destination", read_only=True)
    unlocodeLastport = serializers.CharField(source="unlocode_lastport", read_only=True)
    typeSpecific = serializers.CharField(source="type_specific", read_only=True)
    dataSource = serializers.CharField(source="data_source", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = VesselLocation
        fields = (
            "imo",
            "mmsi",
            "name",
            "latitude",
            "longitude",
            "etaUtc",
            "atdUtc",
            "course",
            "heading",
            "speed",
            "draught",
            "navigationalStatus",
            "destination",
            "lastPort",
            "callsign",
            "positionReceived",
            "updateTime",
            "unlocodeDestination",
            "unlocodeLastport",
            "typeSpecific",
            "dataSource",
            "createdAt",
        )


class VesselWeatherSerializer(serializers.ModelSerializer):
    imo = serializers.CharField(source="vessel.imo", read_only=True)
    mmsi = serializers.CharField(source="vessel.mmsi", read_only=True)
    name = serializers.CharField(source="vessel.name", read_only=True)
    windSpeed = serializers.CharField(source="wind_speed", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = VesselWeather
        fields = (
            "name",
            "imo",
            "mmsi",
            "temperature",
            "windSpeed",
            "waves",
            "createdAt",
        )
