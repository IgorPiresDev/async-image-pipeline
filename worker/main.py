import io

import redis
import requests as rq
from PIL import Image
from pydantic import BaseModel, Field, HttpUrl


class ImageTaskSchema(BaseModel):
    task_id: str
    image_url: HttpUrl
    resize_width: int | None = Field(default=None, gt=0)
    resize_height: int | None = Field(default=None, gt=0)

def Image_process(task:ImageTaskSchema):
    print('Starting the task process:', task.task_id)

    try:
        response= rq.get(str(task.image_url), timeout= 10)
        response.raise_for_status()

        image= Image.open(io.BytesIO(response.content))

        print(f'Image detected, format: {image.format}')
        print(f'Image size: {image.size[0]},{image.size[1]}')
        print(f'Colors: {image.mode}')
        print(f'Download size: {len(response.content) / 1024:.2f} KB')

    except rq.RequestException as e:
        print(f'Conection error for task: {task.task_id}: {e}')

def start_worker():
    r= redis.Redis('localhost', port=6379, db=0, decode_responses=True)
    while True:
        responseRedis= r.blpop('image_tasks', timeout=0)
        if responseRedis is None:
            continue

        taskDataRaw=responseRedis[1]
        try:
            task = ImageTaskSchema.model_validate_json(taskDataRaw)
            Image_process(task)
        except Exception as e:  # noqa: BLE001
            print(f"Error to process the task: {e}")

if __name__=='__main__':
    start_worker()
