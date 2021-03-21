from django.urls import path, include

from rest_framework import routers

from .views import ReceiptViewSet


router = routers.DefaultRouter()
router.register(r'', ReceiptViewSet)

urlpatterns = router.urls
