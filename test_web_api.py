import requests
import json

# Test the web API
url = "http://localhost:5000/api/ultimate-analysis"
data = {"query": "My phone is hacked"}

response = requests.post(url, json=data)
result = response.json()

print("Status Code:", response.status_code)
print("Success:", result.get("success", False))
if result.get("success"):
    print("Domain:", result.get("domain"))
    print("Subdomain:", result.get("subdomain"))
    print("Constitutional Articles:", len(result.get("constitutional_articles", [])))
    print("BNS Sections:", len(result.get("bns_sections", [])))
    print("IPC Sections:", len(result.get("ipc_sections", [])))
    print("CrPC Sections:", len(result.get("crpc_sections", [])))
    
    # Print top constitutional articles
    print("\nTop Constitutional Articles:")
    for article in result.get("constitutional_articles", [])[:3]:
        print(f"  Article {article['article_number']}: {article['title']} ({article['confidence_percentage']}% confidence)")
else:
    print("Error:", result.get("error", "Unknown error"))