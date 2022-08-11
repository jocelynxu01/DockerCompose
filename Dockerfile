FROM python:3.9-slim as base

RUN mkdir /app

COPY requirements.txt  /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app/main.py
COPY model.py /app/model.py
COPY tasks.py /app/tasks.py
COPY minio_storage.py /app/minio_storage.py

WORKDIR /app

FROM base as frontend
CMD ["uvicorn", "main:fastapi_app"]

FROM base as celery_app
CMD ["celery", "-A", "tasks.celery_app", "worker", "-l", "INFO", "-E"]

FROM base as flower_app
CMD ["celery", "flower", "-A", "tasks.celery_app"]