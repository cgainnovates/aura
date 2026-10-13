import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("AURA_BASE_URL")
api_key = os.getenv("AURA_API_KEY")

print("Base URL:", base_url)
print("Key loaded:", bool(api_key))

if not base_url or not api_key:
    raise SystemExit("Missing values. Check that .env is in the project root.")

response = requests.get(
    f"{base_url}/models",
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=30,
)

print("Status:", response.status_code)

if response.status_code == 200:
    for model in response.json()["data"]:
        print(model["id"])
else:
    print(response.text)