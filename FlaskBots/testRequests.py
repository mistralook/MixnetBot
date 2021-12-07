import requests

from utils.coding import b64to_bytes

response = requests.get("http://localhost:8000/public-key")

print(b64to_bytes(response.json()['public_key']))

