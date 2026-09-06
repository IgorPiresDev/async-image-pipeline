from fastapi import FastAPI
from schemas import TaskResponse, ImageTaskPayload
from queue_service import QueueService
import uuid

app = FastAPI(
    title="Cloud Pipeline API",
    version="1.0.0"
)

queue_service = QueueService()


@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.post('/tasks',response_model=TaskResponse, status_code=202)
def create_task(payload: ImageTaskPayload):
    payload_dict = payload.model_dump(mode="json")
    task_id = str(uuid.uuid4())
    queue_service.publish_task(task_id, payload_dict)
    return {
        'task_id': task_id,
        'status': 'QUEUED',
        'message': 'Image Processing task in QUEUED sucefully'
    }
