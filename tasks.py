import time
from celery import Celery
from minio_storage import minio_client
from uuid import UUID
import fitz
from model import predict_bookmark

CELERY_BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

celery_app = Celery('bookmarking')
celery_app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND
)

@celery_app.task(name='slow_addition')
def slow_addition(x: int, y: int):
    time.sleep(15)
    return x + y

@celery_app.task(name='bookmark')
def bookmark(task_id: UUID):
    response = minio_client.get_object(
        bucket_name=str(task_id),
        object_name=f"{task_id}.pdf"
    )

    predictions = []
    with fitz.open(stream=response.data) as document:
        for page in document:
            text = page.get_text()
            prediction = predict_bookmark(text)
            predictions.append(prediction)
    return predictions
