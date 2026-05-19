import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://datadocked.com/api/vessels_operations/get-vessel-info?imo_or_mmsi=9218301"

headers = {
    "accept": "application/json",
    "x-api-key": os.getenv("DATA_DOCKED_API_KEY")
}

response = requests.get(url, headers=headers)
print(response.json())