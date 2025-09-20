# Law Agent Backend API Integration Guide

This guide explains how to integrate with the Law Agent backend API endpoints that are now successfully deployed and accessible.

## Service URL

The backend is deployed at: `https://law-agent-by-grok-1.onrender.com`

## Available API Endpoints

### 1. Health and Status Endpoints

#### GET `/api/ping`
Simple endpoint to verify API accessibility.
- **Response**: 
  ```json
  {
    "success": true,
    "message": "API is accessible",
    "timestamp": "2025-09-20T10:30:45.123456",
    "service": "Ultimate Legal Agent API"
  }
  ```

#### GET `/api/health`
Health check endpoint to verify service status.
- **Response**:
  ```json
  {
    "success": true,
    "status": "healthy",
    "timestamp": "2025-09-20T10:30:45.123456",
    "components": {
      "ultimate_agent": true,
      "web_server": true,
      "session_management": true,
      "query_storage": true,
      "feedback_system": true
    },
    "version": "Ultimate Legal Agent Web Interface v2.0"
  }
  ```

#### GET `/api`
Lists all available API endpoints.
- **Response**:
  ```json
  {
    "message": "Available API endpoints",
    "endpoints": {
      "GET /api/ping": "Simple ping endpoint to verify API accessibility",
      "POST /api/ultimate-analysis": "Process legal queries and get analysis",
      "POST /api/feedback": "Submit feedback for queries",
      "GET /api/history": "Get query history",
      "GET /api/search-history": "Search query history",
      "GET /api/stats": "Get system statistics",
      "GET /api/health": "Health check endpoint",
      "GET /api": "This endpoint - list all API endpoints"
    },
    "timestamp": "2025-09-20T10:30:45.123456"
  }
  ```

### 2. Legal Analysis Endpoints

#### POST `/api/ultimate-analysis`
Process legal queries and get comprehensive analysis.
- **Request Body**:
  ```json
  {
    "query": "What are the IPC sections for murder?"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "query": "What are the IPC sections for murder?",
    "domain": "Criminal Law",
    "subdomain": "Murder And Homicide",
    "domain_confidence": 0.98,
    "bns_sections": ["Section 100", "Section 101"],
    "ipc_sections": ["Section 300", "Section 302", "Section 304"],
    "crpc_sections": ["Section 299", "Section 300"],
    "legal_guidance": "Based on your query about murder...",
    "formatted_response": "Legal Analysis:\n1. Relevant Sections:\n...",
    "total_sections": 7
  }
  ```

#### POST `/api/feedback`
Submit feedback for queries to improve confidence.
- **Request Body**:
  ```json
  {
    "query": "What are the IPC sections for murder?",
    "domain": "criminal_law",
    "subdomain": "murder",
    "confidence": 0.95,
    "feedback": "The analysis was very helpful",
    "rating": 5
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Feedback processed successfully",
    "confidence_adjustment": 0.02,
    "new_confidence": 0.97
  }
  ```

### 3. Data Retrieval Endpoints

#### GET `/api/history`
Get query history.
- **Response**:
  ```json
  {
    "success": true,
    "session_history": [...],
    "agent_history": [...],
    "total_session_queries": 5,
    "total_agent_queries": 10
  }
  ```

#### GET `/api/search-history?q=query`
Search query history.
- **Response**:
  ```json
  {
    "success": true,
    "search_term": "murder",
    "results": [...],
    "count": 3
  }
  ```

#### GET `/api/stats`
Get system statistics.
- **Response**:
  ```json
  {
    "success": true,
    "timestamp": "2025-09-20T10:30:45.123456",
    "legal_coverage": {
      "bns_sections": 358,
      "ipc_sections": 418,
      "crpc_sections": 238,
      "total_sections": 1014
    },
    "query_history": {
      "total_queries": 150
    }
  }
  ```

## CORS Configuration

The API is configured with proper CORS headers to allow requests from any origin:
- **Allowed Origins**: `*` (all origins)
- **Allowed Methods**: `GET, POST, PUT, DELETE, OPTIONS`
- **Allowed Headers**: `Content-Type, Authorization, X-Requested-With, Accept`
- **Credentials**: Supported

## Frontend Integration Examples

### JavaScript Fetch API Example

```javascript
// Ping the API to check connectivity
async function pingAPI() {
  try {
    const response = await fetch('https://law-agent-by-grok-1.onrender.com/api/ping');
    const data = await response.json();
    console.log('API Status:', data);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Analyze a legal query
async function analyzeLegalQuery(query) {
  try {
    const response = await fetch('https://law-agent-by-grok-1.onrender.com/api/ultimate-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query })
    });
    
    const data = await response.json();
    if (data.success) {
      console.log('Analysis Result:', data);
      return data;
    } else {
      console.error('Analysis failed:', data.message);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Submit feedback
async function submitFeedback(query, domain, subdomain, confidence, feedback, rating) {
  try {
    const response = await fetch('https://law-agent-by-grok-1.onrender.com/api/feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        domain: domain,
        subdomain: subdomain,
        confidence: confidence,
        feedback: feedback,
        rating: rating
      })
    });
    
    const data = await response.json();
    console.log('Feedback Result:', data);
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Axios Example

```javascript
import axios from 'axios';

const API_BASE_URL = 'https://law-agent-by-grok-1.onrender.com';

// Ping API
async function pingAPI() {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/ping`);
    console.log('API Status:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// Analyze legal query
async function analyzeLegalQuery(query) {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/ultimate-analysis`, {
      query: query
    });
    console.log('Analysis Result:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}
```

## Error Handling

All API endpoints return consistent error responses:
- **404**: Endpoint not found
- **500**: Internal server error
- **400**: Bad request (missing or invalid parameters)

Error response format:
```json
{
  "error": "Error message",
  "success": false,
  "message": "Human readable error description"
}
```

## Testing the API

You can test the API endpoints using:
1. The provided `test_api_endpoints.ps1` PowerShell script
2. The `frontend_integration_example.html` file
3. curl commands:
   ```bash
   curl -X GET https://law-agent-by-grok-1.onrender.com/api/ping
   curl -X POST https://law-agent-by-grok-1.onrender.com/api/ultimate-analysis -H "Content-Type: application/json" -d '{"query":"What are IPC sections for theft?"}'
   ```

## Troubleshooting

1. **CORS Issues**: Make sure your frontend is making requests with proper headers
2. **Timeout Errors**: Some analysis operations may take time, ensure your frontend handles timeouts appropriately
3. **500 Errors**: Check the query format and ensure all required fields are provided

## Rate Limiting

The API does not currently implement rate limiting, but please use it responsibly to ensure availability for all users.