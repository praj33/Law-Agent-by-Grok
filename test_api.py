import requests
import json

# Test the API endpoint
url = "http://localhost:5000/api/ultimate-analysis"
data = {"query": "My child was kidnapped for ransom"}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", str(e))