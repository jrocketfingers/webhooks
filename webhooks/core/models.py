from django.db import models

from webhooks.core import tasks


class Event(models.Model):
    name = models.CharField(max_length=255)

    def fire(self, payload):
        for webhook in self.webhooks.all():
            result = tasks.call_webhook.delay(webhook.url, payload)
            WebhookJob.objects.create(
                webhook=webhook, payload=payload, result_id=result.id
            )


class Webhook(models.Model):
    event = models.ForeignKey(
        "core.Event", on_delete=models.CASCADE, related_name="webhooks"
    )
    url = models.URLField()


class WebhookJob(models.Model):
    webhook = models.ForeignKey("core.Webhook", on_delete=models.CASCADE)
    payload = models.TextField()
    result_id = models.UUIDField()
