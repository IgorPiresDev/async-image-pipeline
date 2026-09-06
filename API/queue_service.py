import json
from typing import Dict, Any
import redis
import boto3
import logging

class QueueService:
    def __init__(self, queue_name:str='image_task'):
        self.queue_name = queue_name
        self.client = redis.Redis(host= 'redis-service', port= 6379)

    def publish_task(self, task_id: str, payload: dict):
        message= {
            'task_id': task_id,
            'payload': payload
        }
        message_body = json.dumps(message)
        print(f'Despaching for the queue {self.queue_name} : {message_body}')
        self.client.rpush(self.queue_name, message_body)
        return True

queue_service = QueueService()