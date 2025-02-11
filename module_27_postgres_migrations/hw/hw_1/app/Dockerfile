FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flask_app.py .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "flask_app:app"]