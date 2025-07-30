FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 필요한 시스템 패키지 설치 (예: psycopg2 등 의존성 처리)
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && gunicorn CCK_Recorder_OTA_Server.wsgi:application --bind 0.0.0.0:8000"]