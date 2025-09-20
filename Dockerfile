FROM python:3.9.15-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose default port 5000
EXPOSE 5000

# Use a startup script to handle the PORT environment variable
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} ultimate_web_interface:app"]