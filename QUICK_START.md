# 🚀 Legal Agent - Quick Start Commands

## ⚡ Essential Commands

### 1. Setup (One-time)
```bash
# Navigate to project
cd "c:\Users\adity\OneDrive\Desktop\Law Agent by Grok"

# Activate environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt
```

### 2. Test Everything
```bash
# Run comprehensive tests (RECOMMENDED FIRST)
python comprehensive_test.py
```
**Expected**: `✅ System is ready for production!`

### 3. Interactive CLI Agent
```bash
# Start interactive interface
python cli_interface.py

# Example queries to try:
> My landlord won't return my deposit in Mumbai
> My elderly mother is being abused in Delhi
> I want to divorce my husband
> feedback helpful
> stats
> quit
```

### 4. Web API Server
```bash
# Start FastAPI server
uvicorn main:app --reload

# Access at: http://127.0.0.1:8000
# Docs at: http://127.0.0.1:8000/docs
```

### 5. Python API Usage
```python
from legal_agent import create_legal_agent, LegalQueryInput

agent = create_legal_agent()
query = LegalQueryInput(user_input="Your legal question here")
response = agent.process_query(query)
print(response.to_json())
```

## 📊 Data Integration Commands

### View Current Data
```bash
# Test data integration
python data_integration.py

# Check crime statistics
python -c "
from data_integration import CrimeDataAnalyzer
analyzer = CrimeDataAnalyzer()
print('High-risk states:', [s.state_ut for s in analyzer.get_high_risk_states(50)[:5]])
"
```

### Add Your Crime Data
1. **Replace `crime_data.json`** with your JSON data
2. **Ensure same structure**:
   ```json
   {
     "table_6A.1_crime_against_senior_citizens_state_ut_wise_2020_2022": {
       "STATES": [
         {
           "State/UT": "State Name",
           "2020": 123,
           "2021": 456,
           "2022": 789,
           "Actual Senior Citizen Population (in Lakhs) (2011)": 12.3,
           "Rate of Total Crime against Senior Citizen (2022)": 45.6,
           "Chargesheeting Rate (2022)": 78.9
         }
       ],
       "UNION TERRITORIES": [...]
     }
   }
   ```
3. **Test integration**: `python data_integration.py`

## 🧪 Testing Commands

### Full System Test
```bash
python comprehensive_test.py
```

### Individual Component Tests
```bash
# Test domain classification
python -c "
from legal_agent import create_legal_agent, LegalQueryInput
agent = create_legal_agent()
response = agent.process_query(LegalQueryInput(user_input='My landlord issue'))
print(f'Domain: {response.domain}, Confidence: {response.confidence:.2f}')
"

# Test data integration
python -c "
from data_integration import CrimeDataAnalyzer
analyzer = CrimeDataAnalyzer()
advice = analyzer.get_location_based_advice('Delhi', 'senior_citizen_abuse')
print(f'Delhi advice available: {advice[\"location_found\"]}')
"
```

## 🔧 Troubleshooting Commands

### Check System Status
```bash
# Quick health check
python -c "
from legal_agent import create_legal_agent
try:
    agent = create_legal_agent()
    print('✅ System: OK')
    print(f'📊 Data integration: {\"✅\" if agent.data_integration_enabled else \"❌\"}')
    print(f'📈 Feedback entries: {agent.get_feedback_stats()[\"total_feedback\"]}')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Fix Common Issues
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Reset feedback file
echo "timestamp,query,domain,feedback,session_id" > feedback.csv

# Check data file
python -c "
import json
try:
    with open('crime_data.json') as f:
        data = json.load(f)
    print('✅ Crime data loaded successfully')
    print(f'📊 States: {len(data[\"table_6A.1_crime_against_senior_citizens_state_ut_wise_2020_2022\"][\"STATES\"])}')
except Exception as e:
    print(f'❌ Data error: {e}')
"
```

## 📈 Performance Commands

### Benchmark System
```bash
# Performance test
python -c "
import time
from legal_agent import create_legal_agent, LegalQueryInput

agent = create_legal_agent()
start = time.time()
response = agent.process_query(LegalQueryInput(user_input='Performance test'))
end = time.time()

print(f'⚡ Response time: {end-start:.2f}s')
print(f'📋 Domain: {response.domain}')
print(f'🎯 Confidence: {response.confidence:.2f}')
"
```

### View Statistics
```bash
# System statistics
python -c "
from legal_agent import create_legal_agent
agent = create_legal_agent()
stats = agent.get_feedback_stats()
print(f'📊 Total feedback: {stats[\"total_feedback\"]}')
print(f'📈 Positive feedback: {stats[\"positive_percentage\"]:.1f}%')
if stats['domains']:
    print('🏛️  Top domains:', list(stats['domains'].keys())[:3])
"
```

## 🌐 API Testing Commands

### Test FastAPI Endpoints
```bash
# Start server in background
start /B uvicorn main:app --reload

# Test API (requires curl or use Postman)
curl -X POST "http://127.0.0.1:8000/legal-query" ^
     -H "Content-Type: application/json" ^
     -d "{\"user_input\": \"My landlord won't return deposit\", \"feedback\": null}"

# Or use Python requests
python -c "
import requests
response = requests.post(
    'http://127.0.0.1:8000/legal-query',
    json={'user_input': 'Test API query', 'feedback': None}
)
print(f'Status: {response.status_code}')
print(f'Domain: {response.json()[\"domain\"]}')
"
```

## 📁 File Structure Commands

### View Project Structure
```bash
# List all important files
dir /B *.py *.json *.csv *.md

# Check file sizes
for %f in (*.py *.json *.csv) do @echo %f: & @wc -l "%f" 2>nul || @find /c /v "" "%f"
```

### Backup Important Files
```bash
# Create backup
mkdir backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%
copy *.py backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
copy *.json backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
copy *.csv backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
```

## 🎯 Production Deployment Commands

### Production Test
```bash
# Full production readiness test
python comprehensive_test.py > production_test_results.txt
type production_test_results.txt | findstr "Overall Score"
```

### Environment Setup for Production
```bash
# Create production environment file
echo FEEDBACK_FILE=production_feedback.csv > .env
echo ENABLE_DATA_INTEGRATION=true >> .env
echo LOG_LEVEL=INFO >> .env

# Production server start
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🎉 Quick Success Check

Run these commands in order to verify everything works:

```bash
# 1. Test system
python comprehensive_test.py

# 2. Try CLI
python cli_interface.py
# Type: My landlord issue in Mumbai
# Type: quit

# 3. Test API
python -c "from legal_agent import create_legal_agent; print('✅ API works' if create_legal_agent() else '❌ API error')"

# 4. Check data
python -c "from data_integration import CrimeDataAnalyzer; print('✅ Data works' if CrimeDataAnalyzer().crime_stats else '❌ Data error')"
```

**If all show ✅, your system is ready!**

---

**📞 Need Help?**
- Run: `python comprehensive_test.py` for full diagnostics
- Check: `test_report.json` for detailed results
- Use: `python cli_interface.py` and type `help`
