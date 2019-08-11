from rest_framework.routers import DefaultRouter

from webhooks.core.views import EventViewSet
from webhooks.core.views import WebhookViewSet


router = DefaultRouter()
router.register('event', EventViewSet)
router.register('webhook', WebhookViewSet)

urlpatterns = router.urls
