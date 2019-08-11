import requests
from celery import shared_task


@shared_task
def call_webhook(url, payload):
    response = requests.post(url, data=payload)

    return str(response)
