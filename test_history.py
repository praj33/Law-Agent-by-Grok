import requests
import json

# Get query history
url = "http://localhost:5000/api/history"

response = requests.get(url)
result = response.json()

print("Query History:")
print(json.dumps(result, indent=2))