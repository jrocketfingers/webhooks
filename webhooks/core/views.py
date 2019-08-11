from rest_framework import viewsets

from webhooks.core.models import Event, Webhook
from webhooks.core.serializers import EventSerializer, WebhookSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    class Meta:
        model = Event


class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

    class Meta:
        model = Webhook
