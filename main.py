from fastapi import FastAPI, File, UploadFile
from tasks import celery_app
from celery.result import AsyncResult

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
    return {
        'task_id': celery_app_result.id,
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
        'status': celery_app_result.status,
        'result': celery_app_result.result
    }