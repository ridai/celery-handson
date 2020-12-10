from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time

@shared_task
def hello(body: str) -> None:
    time.sleep(10)
    print(body)
