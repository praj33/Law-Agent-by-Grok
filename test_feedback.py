import requests
import json

# First, classify a query
url = "http://localhost:5000/api/ultimate-analysis"
data = {
    "query": "My child was kidnapped for ransom"
}

response = requests.post(url, json=data)
result = response.json()

print("Classification Result:")
print(json.dumps(result, indent=2))

# Now submit feedback
if result.get('success'):
    feedback_url = "http://localhost:5000/api/feedback"
    feedback_data = {
        "query": result['query'],
        "domain": result['domain_raw'],
        "subdomain": result['subdomain_raw'],
        "confidence": result['domain_confidence'],
        "feedback": "This analysis was very helpful and accurate",
        "rating": 5
    }
    
    feedback_response = requests.post(feedback_url, json=feedback_data)
    feedback_result = feedback_response.json()
    
    print("\nFeedback Result:")
    print(json.dumps(feedback_result, indent=2))