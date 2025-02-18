import time
import random
from celery import shared_task

@shared_task
def task_1(task_id):
    duration = random.randint(5, 15)
    time.sleep(duration)
    result = f'Task {task_id} completed after {duration} seconds.'
    return result


