from minio import Minio
from minio.error import S3Error
from uuid import UUID
import logging
import io

MINIO_ENDPOINT = 'localhost:9000'
MINIO_ACCESS_KEY = 'minio'
MINIO_SECRET_KEY = 'minio123'

minio_client = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def upload_to_minio(
        data: bytes,
        task_id: UUID,
        minio_client_instance: Minio = minio_client
):
    """
    Method to upload validated pdf to minio.

    Parameters
    ----------
    minio_client_instance : Minio
    task_id : UUID
    data : bytes

    Returns
    -------

    Raises
    ------

    """
    task_id = str(task_id)
    try:
        minio_client_instance.make_bucket(task_id)

    except S3Error as e:
        if e.code in {"BucketAlreadyOwnedByYou", "BucketAlreadyExists"}:
            logging.warning(
                f"Failed to make bucket `{task_id}` with exception: {e}"
            )
        else:
            logging.error(f"Failed to make bucket name {task_id}")
            raise e

    filename = f"{task_id}.pdf"

    try:
        value_as_a_stream = io.BytesIO(data)
        minio_client_instance.put_object(
            bucket_name=task_id,
            object_name=filename,
            data=value_as_a_stream,
            length=len(data)
        )

    except S3Error as e:
        logging.error(
            f"Could not upload {filename} to Bucket Name {task_id} "
            f"with exception: {e}"
        )
        raise e
