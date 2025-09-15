import requests
import json

url = "http://localhost:5000/api/ultimate-analysis"
data = {"query": "My phone is hacked"}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))