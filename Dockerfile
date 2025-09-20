FROM python:3.9.15-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories if they don't exist
RUN mkdir -p templates static

# Expose default port 5000
EXPOSE 5000

# Use a startup script to handle the PORT environment variable
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 --timeout 120 --keep-alive 5 ultimate_web_interface:app"]