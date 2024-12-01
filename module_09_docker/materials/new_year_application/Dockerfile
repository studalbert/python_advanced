FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY static/ static/
COPY templates/ templates/
COPY app.py app.py

ENTRYPOINT ["python", "app.py"]