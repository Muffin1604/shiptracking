import requests

# Example coordinates
latitude = 19.0760
longitude = 72.8777

url = "https://marine-api.open-meteo.com/v1/marine"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": [
        "wave_height",
        "wave_direction",
        "wave_period",
        "sea_surface_temperature",
        "ocean_current_velocity",
        "ocean_current_direction"
    ],
    "timezone": "auto"
}

response = requests.get(url, params=params)

data = response.json()

print(data)