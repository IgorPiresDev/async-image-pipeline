from typing import Optional
from pydantic import BaseModel,HttpUrl,Field


class ImageTaskPayload(BaseModel):
    image_url: HttpUrl
    target_format: str = 'webp'
    resize_width: Optional[int] = Field(default=None,gt=0)
    resize_height: Optional[int] = Field(default=None,gt=0)
    apply_watermark: bool = False

class TaskResponse(BaseModel):
    task_id: str
    status:str
    message: str