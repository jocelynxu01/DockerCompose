import time
from celery import Celery

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
