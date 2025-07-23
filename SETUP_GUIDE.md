# 🏛️ Legal Agent System - Complete Setup & Usage Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Installation & Setup](#installation--setup)
3. [Running All Agents](#running-all-agents)
4. [Data Integration Guide](#data-integration-guide)
5. [Usage Examples](#usage-examples)
6. [Troubleshooting](#troubleshooting)

## 🎯 System Overview

The Legal Agent System is a production-ready AI-powered legal assistant with:
- **10 Legal Domains**: tenant rights, family law, criminal law, elder abuse, cyber crime, etc.
- **Real Crime Data Integration**: State-wise crime statistics (2020-2022)
- **Multiple Interfaces**: CLI, FastAPI, Python API
- **80% System Performance**: Ready for production use

## 🛠️ Installation & Setup

### Step 1: Environment Setup
```bash
# Navigate to project directory
cd "c:\Users\adity\OneDrive\Desktop\Law Agent by Grok"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Verify Installation
```bash
# Test the system
python comprehensive_test.py
```

Expected output: `✅ System is ready for production!`

## 🚀 Running All Agents

### 1. Comprehensive Testing Agent
**Purpose**: Tests all system functionality and generates performance report
```bash
python comprehensive_test.py
```
**Output**: 
- Classification accuracy: 87.5%
- Route quality: 75%
- Location extraction: 100%
- Data integration: 100%
- Overall score: 80%

### 2. CLI Interactive Agent
**Purpose**: Interactive command-line interface for real-time queries
```bash
python cli_interface.py
```
**Commands**:
- Type any legal question directly
- `help` - Show available commands
- `stats` - View feedback statistics
- `feedback helpful` - Rate responses
- `quit` - Exit

**Example Session**:
```
> My landlord won't return my deposit in Mumbai
📋 Domain: Tenant Rights (Confidence: 0.42)
⏱️  Timeline: 2-3 months
🎯 Expected Outcome: Deposit refund, rent reduction, or lease termination
...

> feedback helpful
✅ Thank you for your feedback: helpful
```

### 3. FastAPI Web Server
**Purpose**: REST API server for web applications
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
**Access**:
- API: http://127.0.0.1:8000
- Interactive Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

**API Endpoint**:
```bash
curl -X POST "http://127.0.0.1:8000/legal-query" \
     -H "Content-Type: application/json" \
     -d '{"user_input": "My employer fired me unfairly", "feedback": null}'
```

### 4. Python API Agent
**Purpose**: Direct Python integration
```python
from legal_agent import create_legal_agent, LegalQueryInput

# Create agent
agent = create_legal_agent()

# Process query
query = LegalQueryInput(user_input="I want to divorce my husband")
response = agent.process_query(query)

print(f"Domain: {response.domain}")
print(f"Legal Route: {response.legal_route}")
```

### 5. Data Analysis Agent
**Purpose**: Crime data analysis and insights
```python
from data_integration import CrimeDataAnalyzer

# Create analyzer
analyzer = CrimeDataAnalyzer()

# Get high-risk states
high_risk = analyzer.get_high_risk_states(50.0)
print(f"High-risk states: {[s.state_ut for s in high_risk[:5]]}")

# Get location advice
advice = analyzer.get_location_based_advice("Delhi", "senior_citizen_abuse")
print(f"Delhi advice: {advice['advice']}")
```

## 📊 Data Integration Guide

### Current Data Structure
The system uses `crime_data.json` with the following structure:
```json
{
  "table_6A.1_crime_against_senior_citizens_state_ut_wise_2020_2022": {
    "STATES": [
      {
        "State/UT": "Andhra Pradesh",
        "2020": 1860,
        "2021": 1818,
        "2022": 2112,
        "Actual Senior Citizen Population (in Lakhs) (2011)": 48.3,
        "Rate of Total Crime against Senior Citizen (2022)": 43.7,
        "Chargesheeting Rate (2022)": 96.6
      }
    ],
    "UNION TERRITORIES": [...]
  }
}
```

### Adding New Crime Data

#### Method 1: Replace Existing Data
1. **Backup current data**:
   ```bash
   copy crime_data.json crime_data_backup.json
   ```

2. **Replace with new data**:
   - Open `crime_data.json` in text editor
   - Replace entire content with your new JSON data
   - Ensure same structure as above

3. **Test integration**:
   ```bash
   python data_integration.py
   ```

#### Method 2: Add New Data Categories
1. **Edit `data_integration.py`**:
   ```python
   # Add new data processing in CrimeDataAnalyzer.__init__()
   def load_data(self):
       # ... existing code ...
       
       # Add new data category
       if "your_new_data_category" in data:
           self._process_new_data(data["your_new_data_category"])
   ```

2. **Add processing method**:
   ```python
   def _process_new_data(self, new_data):
       # Process your new data format
       for item in new_data:
           # Extract and store relevant information
           pass
   ```

### Data Requirements
Your JSON data should include:
- **State/UT names**: For location matching
- **Numerical data**: Crime counts, rates, percentages
- **Time series**: Multiple years for trend analysis
- **Population data**: For rate calculations

### Supported Data Formats
1. **Crime Statistics**: Any crime-related numerical data
2. **Legal Case Data**: Court case statistics
3. **Law Enforcement Data**: Police, prosecution rates
4. **Demographic Data**: Population, age groups
5. **Geographic Data**: State, district, city level

## 💡 Usage Examples

### Example 1: Tenant Rights Query
```bash
python cli_interface.py
> My landlord in Mumbai won't return my security deposit after 3 months
```
**Expected Response**:
- Domain: Tenant Rights
- Legal Route: Send legal notice and approach rent tribunal
- Timeline: 2-3 months
- Process Steps: 8 detailed steps
- Glossary: Legal notice, tribunal definitions

### Example 2: Elder Abuse with Location Data
```bash
> My elderly father is being neglected in a Delhi nursing home
```
**Expected Response**:
- Domain: Elder Abuse
- Location Insights: Delhi crime statistics
- Risk Assessment: Based on local data
- Data-Driven Advice: Location-specific recommendations

### Example 3: API Integration
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/legal-query",
    json={
        "user_input": "I was in a car accident and need compensation",
        "feedback": None
    }
)

result = response.json()
print(f"Domain: {result['domain']}")
print(f"Timeline: {result['timeline']}")
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'legal_agent'`
**Solution**:
```bash
# Ensure you're in the correct directory
cd "c:\Users\adity\OneDrive\Desktop\Law Agent by Grok"

# Activate virtual environment
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Data Integration Disabled
**Problem**: `⚠️ Data integration not available`
**Solution**:
```bash
# Check if crime_data.json exists
dir crime_data.json

# If missing, ensure the file is in the project root
# Test data integration
python data_integration.py
```

#### 3. FastAPI Server Issues
**Problem**: Server won't start
**Solution**:
```bash
# Check if port is available
netstat -an | findstr :8000

# Use different port
uvicorn main:app --reload --port 8001

# Or kill existing process and retry
```

#### 4. Low Classification Accuracy
**Problem**: Poor domain classification
**Solution**:
```python
# Add training examples
from legal_agent import create_legal_agent

agent = create_legal_agent()
agent.add_training_example("cyber crime", "my bank account was hacked online fraud")
```

### Performance Optimization

#### 1. Improve Response Time
```python
# Disable data integration for faster responses
agent = LegalAgent(enable_data_integration=False)
```

#### 2. Batch Processing
```python
# Process multiple queries efficiently
queries = [
    LegalQueryInput(user_input="query1"),
    LegalQueryInput(user_input="query2"),
]

responses = [agent.process_query(q) for q in queries]
```

### System Monitoring
```bash
# Check system performance
python comprehensive_test.py

# View detailed test report
type test_report.json

# Monitor feedback statistics
python -c "from legal_agent import create_legal_agent; print(create_legal_agent().get_feedback_stats())"
```

## 📞 Support

### Getting Help
1. **Run comprehensive tests**: `python comprehensive_test.py`
2. **Check test report**: Review `test_report.json`
3. **Use CLI help**: Type `help` in CLI interface
4. **Review logs**: Check console output for error messages

### System Status Check
```bash
# Quick system health check
python -c "
from legal_agent import create_legal_agent
agent = create_legal_agent()
print('✅ System operational' if agent else '❌ System error')
print(f'📊 Data integration: {\"✅ Enabled\" if agent.data_integration_enabled else \"❌ Disabled\"}')
"
```

---

**🎉 Your Legal Agent System is now ready for production use!**

**Next Steps**:
1. Run `python comprehensive_test.py` to verify everything works
2. Start with `python cli_interface.py` for interactive testing
3. Launch `uvicorn main:app --reload` for web API access
4. Integrate your custom data using the data integration guide
