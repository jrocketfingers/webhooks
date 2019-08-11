from rest_framework import serializers

from webhooks.core.models import Event, Webhook


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'
