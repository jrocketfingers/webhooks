import time

import pytest
from django.urls import reverse
from model_mommy import mommy

from webhooks import __version__
from webhooks.core import tasks
from webhooks.core.models import WebhookJob


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def event():
    return mommy.make("core.Event")


@pytest.fixture
def webhook(event):
    return mommy.make("core.Webhook", event=event)


@pytest.fixture
def webhook_job(webhook):
    return mommy.make("core.WebhookJob", webhook=webhook)


@pytest.fixture
def unsuccessful_webhook_job():
    pytest.fail("Not implemented")


@pytest.mark.api
@pytest.mark.django_db
def test_event_creation(client):
    response = client.post(reverse("event-list"), data={"name": "test-event"})

    assert response.status_code == 201


@pytest.mark.api
@pytest.mark.django_db
def test_webhook_creation(client, event):
    response = client.post(
        reverse("webhook-list"),
        data={"url": "http://webhook.com/path", "event": event.id},
    )

    assert response.status_code == 201


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.django_db
def test_event_fire(event, webhook, celery_worker, requests_mock):
    requests_mock.post(webhook.url)

    # TODO: replace with HTTP call
    event.fire(payload="...")

    assert WebhookJob.objects.filter(webhook=webhook).count() == 1
    webhook_job = WebhookJob.objects.get(webhook=webhook)
    result = tasks.call_webhook.AsyncResult(str(webhook_job.result_id))
    assert result.wait() == "<Response [200]>"
    assert result.status == "SUCCESS"


@pytest.mark.unitest
@pytest.mark.django_db
def test_call_webhook_task(webhook, webhook_job, requests_mock):
    requests_mock.post(webhook.url)
    tasks.call_webhook(webhook.url, webhook_job.payload)

    history = requests_mock.request_history
    assert requests_mock.call_count == 1
    assert history[0].url == webhook.url.lower()
    assert history[0].text == webhook_job.payload


@pytest.mark.skip("Not implemented yet")
@pytest.mark.integration
def test_webhook_job_retries():
    # GIVEN an webhook job
    # WHEN the webhook job fails
    # THEN the task should be rescheduled for later
    pass


@pytest.mark.skip("Not implemented yet")
@pytest.mark.api
def test_webhook_job_result():
    """
    Show that we can fetch results through the API
    """
    pass


@pytest.mark.skip("Not implemented yet")
@pytest.mark.api
def test_backfill(unsuccessful_webhook_job):
    """
    Show that we can backfill results through the API
    """
    pass
