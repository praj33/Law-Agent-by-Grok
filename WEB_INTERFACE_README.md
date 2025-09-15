# Ultimate Legal Agent Web Interface

The Ultimate Legal Agent web interface provides a user-friendly way to access comprehensive legal analysis for ANY type of legal query.

## Features

- Handles ANY type of legal query (murder, kidnapping, rape, cyber crime, etc.)
- Complete BNS, IPC, and CrPC sections
- Enhanced domain and subdomain classification
- Feedback system with confidence adjustment
- Query storage and history
- Real-time legal analysis

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install with `pip install -r requirements.txt`)

### Starting the Web Interface

1. Navigate to the project directory:
   ```
   cd path/to/your/project
   ```

2. Start the web server:
   ```
   python ultimate_web_interface.py
   ```

3. The server will start on `http://localhost:5000`

### Accessing the Web Interface

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You should see the Ultimate Legal Agent interface

## Using the Interface

1. **Enter a Legal Query**: Type any legal question in the input field
   - Examples: "Someone murdered my brother", "I was raped at work", "Hackers stole my money"
   
2. **Click "Analyze Legal Query"**: The system will process your query and provide:
   - Legal domain and subdomain classification
   - Relevant BNS, IPC, and CrPC sections
   - Legal guidance and procedures
   - Emergency contacts when applicable

3. **Provide Feedback**: Rate the analysis and provide feedback to help improve accuracy

4. **View History**: Load your query history to see previous analyses

## API Endpoints

The web interface also provides REST API endpoints:

- `POST /api/ultimate-analysis` - Process legal queries
- `POST /api/feedback` - Submit feedback
- `GET /api/history` - Get query history
- `GET /api/stats` - Get system statistics
- `GET /api/health` - Health check

## Troubleshooting

### Network Error Issues

If you're seeing "Network error. Please check your connection and try again":

1. **Verify the server is running**:
   - Check that `python ultimate_web_interface.py` is still running
   - Look for the message "Running on http://127.0.0.1:5000"

2. **Check the server address**:
   - The interface should be accessible at `http://localhost:5000`
   - If accessing from another device, use the network IP shown in the startup message

3. **Browser issues**:
   - Try refreshing the page
   - Try using a different browser
   - Check browser console for specific error messages (F12)

4. **Firewall/Security software**:
   - Ensure your firewall isn't blocking the connection
   - Temporarily disable security software to test

### Common Solutions

1. **Restart the server**:
   ```
   # Stop the current server (Ctrl+C)
   # Start it again
   python ultimate_web_interface.py
   ```

2. **Clear browser cache**:
   - Press Ctrl+Shift+R to force refresh
   - Or clear browser cache and cookies

3. **Check for port conflicts**:
   - If port 5000 is in use, modify the port in `ultimate_web_interface.py`

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **RAM**: 2GB minimum recommended
- **Storage**: 500MB free space
- **Browser**: Modern web browser (Chrome, Firefox, Edge, Safari)

## Support

If you continue to experience issues:

1. Check the terminal output for error messages
2. Verify all Python dependencies are installed
3. Ensure you're using a supported browser
4. Contact support with detailed error information