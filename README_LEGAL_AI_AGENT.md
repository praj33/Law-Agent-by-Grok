# Legal AI Agent

A comprehensive legal AI agent that can classify legal queries and retrieve relevant legal provisions from the complete Bharatiya Nyaya Sanhita (BNS 2023), Indian Penal Code (IPC 1860), and Code of Criminal Procedure (CrPC 1973).

## Features

- **Domain & Subdomain Classification**: Automatically classifies legal queries into appropriate legal domains and subdomains
- **Complete Legal Coverage**: Retrieves ALL relevant sections from BNS, IPC, and CrPC (no limit on number of sections)
- **Constitutional Articles**: Provides relevant constitutional articles when applicable
- **Structured Output**: Formats output in a consistent, organized structure
- **Web Interface**: User-friendly web interface for easy interaction
- **Feedback System**: Collects user feedback to improve accuracy
- **Frontend Updates**: Automatically updates frontend with latest analysis

## Requirements

- Python 3.7+
- Flask
- scikit-learn
- pandas
- numpy

## Installation

1. Ensure all required Python packages are installed:
   ```bash
   pip install flask scikit-learn pandas numpy
   ```

2. Make sure all the following files are in the project directory:
   - `legal_ai_agent.py`
   - `legal_ai_web_interface.py`
   - `start_legal_ai_agent.py`
   - `test_legal_ai_agent.py`
   - All existing legal database files (bns, ipc, crpc, constitutional articles, etc.)

## Usage

### Starting the Web Interface

To start the Legal AI Agent web interface:

```bash
python start_legal_ai_agent.py
```

The web interface will be available at: http://localhost:5001

### Using the Web Interface

1. Open your web browser and navigate to http://localhost:5001
2. Enter your legal query in the input field
3. Click "Analyze Legal Query" or press Enter
4. View the comprehensive legal analysis including:
   - Domain and subdomain classification
   - Relevant constitutional articles
   - BNS, IPC, and CrPC sections
   - Step-by-step legal process
   - Important notes and safeguards
   - Emergency contacts (when applicable)
5. Provide feedback using the feedback form to help improve accuracy

### Programmatic Usage

You can also use the Legal AI Agent programmatically:

```python
from legal_ai_agent import create_legal_ai_agent

# Create the agent
agent = create_legal_ai_agent()

# Process a query
result = agent.process_query("My child was kidnapped for ransom")

# Format the output
formatted_output = agent.format_output(result)
print(formatted_output)
```

## Output Structure

The Legal AI Agent provides output in the following structured format:

```
Domain: [Legal Domain]
Subdomain: [Legal Subdomain]

Constitutional Articles:
  • Article [Number]: [Title]
  ...

BNS Sections:
  • Section [Number]: [Title]
    [Description]
  ...

IPC Sections:
  • Section [Number]: [Title]
    [Description]
  ...

CrPC Sections:
  • Section [Number]: [Title]
    [Description]
  ...

Step-by-step Legal Process:
  [Process Steps]

Important Notes / Safeguards:
  • [Note 1]
  • [Note 2]
  ...

Emergency Contacts:
  • [Service]: [Number]
  ...

💬 Feedback Options:
  • Helpful
  • Very Helpful
  • Not Helpful
  • Needs Work
```

## Supported Legal Domains

The Legal AI Agent supports a comprehensive range of legal domains including:

- Criminal Law
- Cyber Law
- Labour & Employment Law
- Family Law
- Property Law
- Consumer Law
- Tort Law
- Corporate Law
- Tax Law
- Banking Law
- Immigration Law
- Constitutional Law
- And many more...

## Testing

To run the test suite:

```bash
python test_legal_ai_agent.py
```

## Architecture

The Legal AI Agent consists of several key components:

1. **ML Domain Classifier**: Uses machine learning to classify legal queries into domains
2. **Subdomain Classifier**: Provides detailed subdomain classification within each domain
3. **Legal Database**: Comprehensive database of all BNS, IPC, and CrPC sections
4. **Constitutional Article Matcher**: Finds relevant constitutional articles for queries
5. **Web Interface**: Flask-based web interface for user interaction
6. **Feedback System**: Collects and processes user feedback to improve accuracy

## Feedback System

The Legal AI Agent includes a feedback system that:
- Collects user ratings (1-5 stars)
- Accepts textual feedback
- Adjusts confidence scores based on feedback
- Stores feedback history for continuous improvement

## Frontend Integration

After every response, the system automatically updates results in the frontend (simple_index.html) so that the web interface always displays the latest analysis, legal provisions, and feedback status.

## Example Queries

Try these example queries to see the Legal AI Agent in action:

- "My child was kidnapped for ransom"
- "Someone murdered my brother in cold blood"
- "I was raped by my colleague"
- "Hackers stole money from my bank account"
- "My boss fired me for reporting harassment"
- "My husband beats me daily"
- "Business partner embezzled funds"
- "Caught with drugs at airport"
- "Landlord won't return security deposit"
- "Company sold defective product"

## Contributing

Contributions to improve the Legal AI Agent are welcome. Please ensure:
1. All tests pass before submitting pull requests
2. Code follows the existing style and structure
3. New features are well-documented
4. Feedback mechanisms are preserved and enhanced

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Legal Agent Team for the foundational components
- Built upon the existing BNS, IPC, CrPC, and constitutional article databases
- Uses scikit-learn for machine learning components
- Flask for web interface implementation