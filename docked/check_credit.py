import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://datadocked.com/api/vessels_operations/my-credits"

headers = {
    "x-api-key": os.getenv("DATA_DOCKED_API_KEY")
}

response = requests.get(url, headers=headers)

print(response.json())