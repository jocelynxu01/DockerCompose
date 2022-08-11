from fastapi import FastAPI, File, UploadFile
from tasks import celery_app
from celery.result import AsyncResult
from uuid import uuid4, UUID

from minio_storage import upload_to_minio

fastapi_app = FastAPI()


@fastapi_app.post("/predict")
async def predict(x: int, y: int, return_pdf: UploadFile = File(...)):

    kwargs = {
        'x': x,
        'y': y
    }

    celery_app_result: AsyncResult = celery_app.send_task(
        'slow_addition',
        kwargs=kwargs
    )


    data: bytes = await return_pdf.read()
    task_id = uuid4()

    upload_to_minio(
        task_id=task_id,
        data=data
    )

    bookmark_async_res: AsyncResult = celery_app.send_task(
        'bookmark',
        [task_id],
        task_id=str(task_id)
    )

    return {
        'task_id': f"{bookmark_async_res.id}",
        'input': {
            'x': x,
            'y': y
        },
        'status': celery_app_result.status,
        'result': celery_app_result.result
    }

@fastapi_app.get("/results")
async def results(task_id: str):
    celery_app_result = AsyncResult(task_id, app=celery_app)
    
    return {
        'task_id': task_id,
        'status': celery_app_result.state,
        'result': celery_app_result.result
    }