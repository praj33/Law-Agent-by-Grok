FROM python:3.9.15-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "ultimate_web_interface:app"]