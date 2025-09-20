import requests
import json

# Get system statistics
url = "http://localhost:5000/api/stats"

response = requests.get(url)
result = response.json()

print("System Statistics:")
print(json.dumps(result, indent=2))